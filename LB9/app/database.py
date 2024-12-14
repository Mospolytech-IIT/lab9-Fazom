from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загрузка конфигурации из .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Настройка подключения
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
