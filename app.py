import csv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from tabulate import tabulate
from sqlalchemy import func
from database import Base, engine, SessionLocal
from models import Expense, Budget, GroupExpense

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

Base.metadata.create_all(bind=engine)
session = SessionLocal()

# --- Functions  ---
# function to add category 
def log_spending():
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    date = datetime.strptime(input("Enter date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    exp = Expense(category=category, amount=amount, date=date)
    session.add(exp)
    session.commit()
    print("Expense added successfully!")
# user set their budget
def assign_budget():
    category = input("Enter budget category: ")
    month = input("Enter month (YYYY-MM): ")
    limit = float(input("Enter budget limit: "))
    b = Budget(category=category, month=month, limit=limit)
    session.add(b)
    session.commit()
    print("Budget saved!")
# to check alerts ex whether  the purchased  has increased  the budget
def check_alerts():
    current_month = datetime.now().strftime("%Y-%m")
    budgets = session.query(Budget).filter(Budget.month == current_month).all()

    for b in budgets:
        spent = session.query(func.sum(Expense.amount)).filter(
            Expense.category == b.category,
            func.strftime("%Y-%m", Expense.date) == current_month
        ).scalar() or 0

        remaining = b.limit - spent

        if b.limit > 0 and remaining <= (0.10 * b.limit) and remaining > 0:
            msg = f"⚠ WARNING: Only 10% budget left for {b.category} — Remaining: {remaining}"
            print(msg)
            send_email_alert(msg)

        if spent > b.limit:
            msg = f"❌ ALERT: Budget exceeded for {b.category} — Spent {spent} / Limit {b.limit}"
            print(msg)
            send_email_alert(msg)
# function to view our report /expense table 
def view_report():
    month = input("Enter month (YYYY-MM): ")
    rows = []
    categories = session.query(Expense.category).distinct()
    for cat in categories:
        spent = session.query(func.sum(Expense.amount)).filter(
            Expense.category == cat[0],
            func.strftime("%Y-%m", Expense.date) == month
        ).scalar() or 0

        budget = session.query(Budget.limit).filter(
            Budget.category == cat[0],
            Budget.month == month
        ).scalar() or 0

        rows.append([cat[0], spent, budget])
    print(tabulate(rows, headers=["Category", "Spent", "Budget"]))
# function to edit our response as per our need
def edit_expense():
    exp_id = int(input("Enter Expense ID to edit: "))
    expense = session.query(Expense).filter(Expense.id == exp_id).first()
    if not expense:
        print("Expense not found.")
        return
    
    new_amount = float(input("Enter new amount: "))
    new_category = input("Enter new category: ")
    new_date = datetime.strptime(input("Enter new date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    
    expense.amount = new_amount
    expense.category = new_category
    expense.date = new_date
    session.commit()
    print("Expense updated successfully!")
# function to delete 
def delete_expense():
    exp_id = int(input("Enter Expense ID to delete: "))
    expense = session.query(Expense).filter(Expense.id == exp_id).first()
    if not expense:
        print("Expense not found.")
        return
    session.delete(expense)
    session.commit()
    print("Expense deleted!")
# function to export our table to csv
def export_csv():
    month = input("Enter month to export (YYYY-MM): ")
    filename = f"report_{month}.csv"
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Amount", "Date"])
        
        expenses = session.query(Expense).filter(
            func.strftime("%Y-%m", Expense.date) == month
        ).all()
        
        for e in expenses:
            writer.writerow([e.category, e.amount, e.date])
    
    print(f"CSV exported successfully: {filename}")
# additional function to send email 
def send_email_alert(msg):
    try:
        email = MIMEText(msg)
        email["Subject"] = "Budget Alert - Expense Tracker"
        email["From"] = EMAIL_SENDER
        email["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email.as_string())

        print(" Email notification sent successfully.")
    except Exception as e:
        print("Email failed!. Check credentials.")
        print(e)
# function to create group expense
def add_group_expense():
    group = input("Enter group name: ")
    member = input("Enter member name: ")
    amount = float(input("Enter amount: "))
    ge = GroupExpense(group_name=group, member=member, amount=amount)
    session.add(ge)
    session.commit()
    print("Group expense added!")
# to obtain group summary
def group_summary():
    group = input("Enter group name: ")
    rows = session.query(GroupExpense.member, func.sum(GroupExpense.amount)).filter(
        GroupExpense.group_name == group).group_by(GroupExpense.member).all()
    
    print("\nExpense distribution among members:")
    for r in rows:
        print(f"{r[0]} → {r[1]}")

# main function
def menu():
    while True:
        print("\n===== MY EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. Set Monthly Budget")
        print("3. Show Spending vs Budget")
        print("4. Check Alerts")
        print("5. Edit Expense")
        print("6. Delete Expense")
        print("7. Export Monthly Report to CSV")
        print("8. Add Group Expense")
        print("9. View Group Summary")
        print("10. Exit")

        choice = input("Select option: ")

        if choice == "1":
            log_spending()
        elif choice == "2":
            assign_budget()
        elif choice == "3":
            view_report()
        elif choice == "4":
            check_alerts()
        elif choice == "5":
            edit_expense()
        elif choice == "6":
            delete_expense()
        elif choice == "7":
            export_csv()
        elif choice == "8":
            add_group_expense()
        elif choice == "9":
            group_summary()
        elif choice == "10":
            print("Thank you for using the Expense Tracker!")
            break
        else:
            print("❌ Invalid choice!. Please try again.")

if __name__ == "__main__":
    menu()
