from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:matvei1@localhost:3306/meme_app")

def get_engine():
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Test the connection
            engine.connect()
            return engine
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to connect to database after {max_retries} attempts: {str(e)}")

engine = get_engine()
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
