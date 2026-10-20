import os

from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI(title="Сервис учета расходов")
load_dotenv()

@app.get("/")
def root():
    return {"message": "Сервис работает"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version":"0.1.0"}

@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Учебный сервис")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    return {
        "app_name": app_name,
        "author": app_author,
    }

