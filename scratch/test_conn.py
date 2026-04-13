import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Add Backend to path
sys.path.append(os.getcwd())

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/habit_tracker")

print(f"Testing connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Successfully connected to MySQL!")
    connection.close()
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
    print("\nChecklist:")
    print("1. Is MySQL service running?")
    print("2. Does the database 'habit_tracker' exist?")
    print("3. Are the credentials in .env correct?")
