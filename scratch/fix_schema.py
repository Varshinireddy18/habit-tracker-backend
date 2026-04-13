
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

def run_migration():
    with engine.connect() as connection:
        # Add days_of_week to habits
        print("Adding 'days_of_week' to 'habits' table...")
        try:
            connection.execute(text("ALTER TABLE habits ADD COLUMN days_of_week VARCHAR(50) DEFAULT '1,2,3,4,5,6,7'"))
            print("Successfully added to 'habits'.")
        except Exception as e:
            print(f"Error updating 'habits': {e}")

        # Add days_of_week to goals
        print("\nAdding 'days_of_week' to 'goals' table...")
        try:
            connection.execute(text("ALTER TABLE goals ADD COLUMN days_of_week VARCHAR(50) DEFAULT '1,2,3,4,5,6,7'"))
            print("Successfully added to 'goals'.")
        except Exception as e:
            print(f"Error updating 'goals': {e}")
            
        connection.commit()

if __name__ == "__main__":
    run_migration()
    print("\nMigration complete.")
