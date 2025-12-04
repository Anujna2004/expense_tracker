from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    amount = Column(Float)
    date = Column(Date)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    month = Column(String)  
    limit = Column(Float)

class GroupExpense(Base):
    __tablename__ = "group_expenses"
    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    member = Column(String)
    amount = Column(Float)
