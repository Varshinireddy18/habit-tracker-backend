
import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "habit_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

def check_table(table_name):
    print(f"\nColumns in '{table_name}':")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

check_table("habit_logs")
