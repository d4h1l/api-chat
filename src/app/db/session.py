from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Объект сессии, через который выполняются запросы
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Базовый класс для всех моделей SQLAlchemy
class Base(DeclarativeBase):
    pass
