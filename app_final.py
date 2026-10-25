import os
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Expense Tracker")

app = FastAPI(title=APP_NAME)

# Хранилище данных
expenses = []
next_id = 1

@app.get("/")
def root():
    logger.info("Запрос к главной странице")
    return {"message": "Expense Tracker API", "app_name": APP_NAME}


@app.get("/health")
def health():
    logger.info("Проверка здоровья (health check)")
    return {"status": "ok"}


@app.get("/version")
def version():
    logger.info("Запрос версии приложения") 
    return {"version":"0.1.0"}

@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Учебный сервис")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    return {
        "app_name": app_name,
        "author": app_author,
    }

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
    logger.info(f"Добавлен новый расход: ID={next_id}, Название='{item['title']}', Сумма={item['amount']}")
    next_id += 1
    return item

@app.get("/expenses")
def get_expenses(category: str = None):
    if category:
        logger.info(f"Запрошен список расходов с фильтром по категории: '{category}'")
        return [e for e in expenses if e["category"] == category]
    logger.info("Запрошен полный список расходов")
    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for e in expenses:
        if e["id"] == expense_id:
            logger.info(f"Найден расход по ID={expense_id}")
            return e
    logger.warning(f"Попытка получить несуществующий расход с ID={expense_id}")
    raise HTTPException(status_code=404, detail="Expense not found")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    global expenses
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            deleted = expenses.pop(i)
            logger.info(f"Удален расход: ID={expense_id}, Название='{deleted['title']}'")
            return {"message": "Expense deleted", "deleted": deleted}
    logger.warning(f"Попытка удалить несуществующий расход с ID={expense_id}")
    raise HTTPException(status_code=404, detail="Expense not found")