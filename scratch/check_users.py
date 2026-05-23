
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "habit_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def check_users():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name, email, total_habits FROM users"))
        for row in result:
            print(f"User: {row[1]} (ID: {row[0]}), total_habits: {row[2]}")

if __name__ == "__main__":
    check_users()
