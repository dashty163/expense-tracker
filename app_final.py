import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

APP_NAME = os.getenv("APP_NAME", "Expense Tracker")

app = FastAPI(title=APP_NAME)
load_dotenv()

expenses = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Expense Tracker API", "app_name": APP_NAME}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version":"0.1.0"}


# --- Маршруты для расходов ---

@app.post("/expenses")
def add_expense(expense: dict):
    global next_id
    item = {
        "id": next_id,
        "title": expense.get("title"),
        "amount": expense.get("amount"),
        "category": expense.get("category")        
    }
    expenses.append(item)
    next_id += 1
    return item

@app.get("/expenses")
def get_expenses(category: str = None):
    if category:
        return [e for e in expenses if e["category"] == category]
    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for e in expenses:
        if e["id"] == expense_id:
            return e
    raise HTTPException(status_code=404, detail="Expense not found")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    global expenses
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            deleted = expenses.pop(i)
            return {"message": "Expense deleted", "deleted": deleted}
    raise HTTPException(status_code=404, detail="Expense not found")