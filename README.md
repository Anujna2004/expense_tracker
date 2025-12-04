# Expense Tracker
#I created this tool to manage monthly spending and compare it with budgets.
The focus was on simple usage and practical tracking.
A simple and powerful command-line Expense Tracker that helps users monitor monthly spending, set budgets, receive alerts, and export reports.


## Steps to Run
pip install -r requirements.txt
python app.py

## Test Cases
1. Add expense
2. Set monthly budget
3. View monthly spending vs budget
4. Check alerts when spending reaches 90% or exceeds budget → alert/email should display
5. Edit expense and verify updated result in reports
6. Delete expense and verify it is removed
7. Export monthly expense report to CSV → CSV file should generate
8. Add group expense
9. View group summary → member-wise total should display
10. Restart the app → all data remains stored because of SQLite persistence

## SQL/ORM Note
Application uses SQLAlchemy ORM with SQLite database.
