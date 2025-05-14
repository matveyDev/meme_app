import os
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
from dotenv import load_dotenv

load_dotenv()

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://user:password@db:3306/meme_db")

# Настройки для повторных попыток подключения
max_retries = 5
retry_delay = 10  # секунды

def get_db_connection():
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={
                    "connect_timeout": 10,
                    "read_timeout": 30,
                    "write_timeout": 30
                }
            )
            # Проверяем подключение
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Successfully connected to database!")
            return engine
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise Exception(f"Failed to connect to database after {max_retries} attempts: {str(e)}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

# Создаем движок базы данных
engine = get_db_connection()
meta = MetaData()

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
