from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

# In-memory database for simplicity
expenses = []

class Expense(BaseModel):
    id: UUID = uuid4()
    date: datetime
    category: str
    amount: float
    description: str

@app.post("/add_expense", response_model=dict)
async def add_expense(expense: Expense):
    expenses.append(expense)
    print("Expense added. Current expenses:", expenses)
    return {"message": "Expense added successfully"}

@app.get("/view_expenses", response_model=List[Expense])
async def view_expenses():
    print("Viewing expenses:", expenses)
    return expenses

@app.get("/view_expenses_by_category", response_model=List[Expense])
async def view_expenses_by_category(category: str):
    filtered_expenses = [exp for exp in expenses if exp.category == category]
    if not filtered_expenses:
        raise HTTPException(status_code=404, detail="No expenses found in the specified category")
    return filtered_expenses

@app.get("/view_total_expenses", response_model=dict)
async def view_total_expenses():
    total_amount = sum(exp.amount for exp in expenses)
    print("Calculating total expenses. Current expenses:", expenses)
    return {"total_amount": total_amount}
