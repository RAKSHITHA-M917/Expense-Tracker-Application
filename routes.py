from flask import Blueprint, request, jsonify
from db import db
from models import Expense, Budget, Group, User
from sqlalchemy import func
from datetime import datetime
from config import Config
from emailer import send_alert_email

bp = Blueprint("api", __name__)

def year_month_from_date(dt):
    if isinstance(dt, str):
        dt_obj = datetime.fromisoformat(dt).date()
    else:
        dt_obj = dt
    return dt_obj.strftime("%Y-%m")

@bp.route("/expense", methods=["POST"])
def api_add_expense():
    """
    Add an expense.
    JSON body: {title, category, amount, date (YYYY-MM-DD, optional), note (optional), group_id (optional), split_count (optional), paid_by_user_id (optional)}
    """
    data = request.get_json() or {}
    title = data.get("title")
    category = data.get("category")
    amount = data.get("amount")
    date_str = data.get("date")
    note = data.get("note")
    group_id = data.get("group_id")
    split_count = data.get("split_count")
    paid_by = data.get("paid_by_user_id")

    if not title or not category or amount is None:
        return jsonify({"error": "title, category and amount are required"}), 400

    try:
        if date_str:
            dt = datetime.fromisoformat(date_str).date()
        else:
            dt = datetime.today().date()

        exp = Expense(
            title=title,
            category=category,
            amount=float(amount),
            date=dt,
            note=note,
            group_id=group_id,
            split_count=int(split_count) if split_count else None,
            paid_by_user_id=paid_by
        )
        db.session.add(exp)
        db.session.commit()

        ym = year_month_from_date(dt)
        spent = db.session.query(func.coalesce(func.sum(
            func.coalesce( (Expense.amount / Expense.split_count) , Expense.amount)
        ), 0.0)).filter(
            func.strftime("%Y-%m", Expense.date) == ym,
            Expense.category == category
        ).scalar() or 0.0

        budget = Budget.query.filter_by(category=category, month=ym).first()
        alert = None
        if budget:
            if spent > budget.amount:
                alert = f"Budget exceeded for {category} in {ym}. Spent {spent:.2f}, budget {budget.amount:.2f}."
            else:
                remaining = budget.amount - spent
                if remaining <= (budget.amount * Config.ALERT_THRESHOLD):
                    alert = f"Only {remaining:.2f} left for {category} in {ym} ({int(Config.ALERT_THRESHOLD*100)}% threshold)."

        email_sent = False
        if alert and exp.paid_by_user_id:
            payer = User.query.get(exp.paid_by_user_id)
            if payer and payer.email:
                email_sent = send_alert_email(
                    payer.email,
                    f"Budget alert for {category} - {ym}",
                    alert
                )

        return jsonify({"expense": exp.to_dict(), "alert": alert, "email_sent": email_sent}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route("/budget", methods=["POST"])
def api_set_budget():
    """
    Set or update budget for a category and month.
    JSON: {category, month (YYYY-MM), amount}
    """
    data = request.get_json() or {}
    category = data.get("category")
    month = data.get("month")
    amount = data.get("amount")
    if not category or not month or amount is None:
        return jsonify({"error": "category, month and amount required"}), 400
    try:
        bud = Budget.query.filter_by(category=category, month=month).first()
        if bud:
            bud.amount = float(amount)
        else:
            bud = Budget(category=category, month=month, amount=float(amount))
            db.session.add(bud)
        db.session.commit()
        return jsonify({"budget": {"category": bud.category, "month": bud.month, "amount": bud.amount}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route("/report/monthly", methods=["GET"])
def api_report_monthly():
    """
    Get total spending per month (overall and per category).
    Query param: month=YYYY-MM
    """
    month = request.args.get("month")
    if not month:
        return jsonify({"error": "month query param required (YYYY-MM)"}), 400

    rows = db.session.query(
        Expense.category,
        func.coalesce(func.sum(
            func.coalesce( (Expense.amount / Expense.split_count), Expense.amount)
        ), 0.0).label("total")
    ).filter(func.strftime("%Y-%m", Expense.date) == month).group_by(Expense.category).all()

    per_category = {r.category: float(r.total) for r in rows}
    total = sum(per_category.values())
    return jsonify({"month": month, "per_category": per_category, "total": total}), 200

@bp.route("/report/compare", methods=["GET"])
def api_report_compare():
    """
    Compare spending vs budget per category for a given month.
    Query param: month=YYYY-MM
    """
    month = request.args.get("month")
    if not month:
        return jsonify({"error": "month required"}), 400

    budgets = Budget.query.filter_by(month=month).all()
    results = {}
    for b in budgets:
        spent = db.session.query(func.coalesce(func.sum(
            func.coalesce( (Expense.amount / Expense.split_count), Expense.amount)
        ), 0.0)).filter(
            func.strftime("%Y-%m", Expense.date) == month,
            Expense.category == b.category
        ).scalar() or 0.0
        pct_used = (spent / b.amount * 100.0) if b.amount > 0 else None
        results[b.category] = {"budget": b.amount, "spent": float(spent), "remaining": float(b.amount - spent), "pct_used": pct_used}
    return jsonify({"month": month, "comparisons": results}), 200

@bp.route("/groups", methods=["POST"])
def api_create_group():
    """Create a group for shared expenses: JSON {name}"""
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400
    g = Group(name=name)
    db.session.add(g)
    db.session.commit()
    return jsonify({"id": g.id, "name": g.name}), 201

@bp.route("/users", methods=["POST"])
def api_create_user():
    """Create a user: JSON {name, email (optional)}"""
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    u = User(name=name, email=email)
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id, "name": u.name, "email": u.email}), 201