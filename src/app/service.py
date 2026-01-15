from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Chat API")

# Подключение роутов
app.include_router(router)
