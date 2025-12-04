# Expense Tracker
#I created this tool to manage monthly spending and compare it with budgets.
The focus was on simple usage and practical tracking.


## Steps to Run
pip install -r requirements.txt
python app.py

## Test Cases
1. Add expense
2. Set category budget
3. Add expenses beyond budget → alert should display
4. View monthly spending vs budget
5. Restart app → all stored because SQLite persistent

## SQL/ORM Note
Application uses SQLAlchemy ORM with SQLite database.
