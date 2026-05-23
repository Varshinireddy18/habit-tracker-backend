import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "habit_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
print(f"Testing connection to: {url} (without DB name first)")

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        print("Connected to MySQL server!")
        result = conn.execute(text("SHOW DATABASES;"))
        databases = [row[0] for row in result]
        print(f"Databases: {databases}")
        if DB_NAME in databases:
            print(f"Database '{DB_NAME}' exists.")
        else:
            print(f"Database '{DB_NAME}' DOES NOT exist.")
except Exception as e:
    print(f"Error: {e}")
