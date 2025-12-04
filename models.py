from db import db
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    """Optional simple user model (email used for notifications)."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=True)

class Group(db.Model):
    """Group to allow shared expenses (simple Splitwise-style)."""
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class Budget(db.Model):
    """
    Budget per category per month.
    month format: YYYY-MM (e.g., 2025-12)
    """
    __tablename__ = "budgets"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    __table_args__ = (db.UniqueConstraint('category', 'month', name='_category_month_uc'),)

class Expense(db.Model):
    """
    Expense record. If group_id present, it's shared with count_shares members.
    If shared, field split_count indicates how many ways it is shared.
    """
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.String(256))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    split_count = db.Column(db.Integer, nullable=True)  
    paid_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    group = db.relationship("Group", backref="expenses")
    payer = db.relationship("User", backref="paid_expenses")

    @hybrid_property
    def effective_amount(self):
        """Amount considered for single user (if split_count set, returns share)."""
        if self.split_count and self.split_count > 0:
            return self.amount / self.split_count
        return self.amount

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "note": self.note,
            "group_id": self.group_id,
            "split_count": self.split_count,
            "paid_by_user_id": self.paid_by_user_id
        }