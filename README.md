Expense Tracker Application
    A simple Python Flask web application to track daily expenses, set monthly budgets, and monitor spending.
Features
    Add daily expenses with   amount, category, note, and date .
    Set monthly budgets for each category.
Alerts:
    If total spent exceeds budget.
    View monthly report:
    Total spending per month.
    Summary of spending vs budget per category.
    Fully functional with Docker.
Tech Stack
    Python 3.11
    Flask
    SQLite (lightweight database)
    HTML/CSS for frontend
    Docker (optional)
Project Structure
    EXPENSE_TRACKER
    > pycache_
    static
    JS app.js
    #style.css
    templates
    <> index.html
    Exercises
    test_api.py
    venv
    Include >
    > Lib
    > Scripts
    pyvenv.cfg
    app.py
    config.py
    db.py
    Dockerfile
    emailer.py
    expense_data.db
    models.py
    requirements.txt
    routes.py
Setup & Run Locally
    1.Fork the repository
        git clone <your-repo-url>
        cd expense-tracker
    2.Create virtual environment and activate
        python -m venv venv
        venv\Scripts\activate   
    3.Install dependencies
        pip install -r requirements.txt
    4.Run the application
        python app.py
    5. Open your browser and go to:
        http://localhost:5000
Docker Commands
    1.Build Docker image
        docker build -t expense-tracker.
    2.Run the container
        docker run -p 5000:5000 expense-tracker
    3.Open your browser:
        http://localhost:5000
Test/Validation Steps
    1. Add Expense
        1. Go to   Add Expense   page.
        2. Type:
        Title (e.g., Lunch)
        Category Food/Travel
        Quantity
        dd-mm-yyyy
        Split count (optional)
        Note (optional)
        3. Click   Add Expense .

        4. You should see a   success flash message .
    2. Establish Budget
        1. Go to   Set Budget   page.
        2. Input:
        Establish Budget
        Category
        Quantity

        3. Click   Set Budget .
        4. You should see   budget added confirmation .
    3. Alert Verification
        Add expenses totaling more than the budget → you should see an   ALERT: Budget exceeded   message.
        Add expenses up to 90% of budget → you should see   WARNING: Low budget   message.
    4. View Monthly Report
        1. Go to   Monthly Report .
        2. Select current month or leave empty for current month.
        3. You should see:
        Reports
        April, 2025
        {
        Get Report
        "monthly":
        "month": "2025-04",
        "per_category":
        "food": 45000
        "total": 45000
        },
        },
        "compare":
        "comparisons":
        "food": {},
        Whoa!
        "budget": 1000,
        "pct_used": 4500,
        "remaining": -44000,
        "spent": 45000
        "month": "2025-04"
        5. Delete Expense
        Click the Delete button in the report → confirm → the expense should be removed.
        6. Budget Update
        Set budget again for the same category → previous budget is   updated .
        Edge Cases / Notes
        Amount must be a  positive number.
        Category cannot be empty.
        Date format should be in the form YYYY-MM-DD.
        Deleting expenses is   irreversible .
        Budget alerts work   per category per month
SQL / ORM
    SQLite queries are used for:
    Add ,Set ,
    Fetch total and monthly summaries.
    `ON CONFLICT` clause handles budget updates.
Conclusion
    Fully functional   expense tracker Monthly report   and   budget alerts SQL query Implementation Docker support