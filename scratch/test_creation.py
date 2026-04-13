
import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, Habit, Goal, User, HabitLog
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "habit_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_creation():
    db = SessionLocal()
    try:
        # 1. Create a dummy user
        user_id = str(uuid.uuid4())
        new_user = User(
            id=user_id,
            name="Test User",
            email=f"test_{uuid.uuid4().hex[:6]}@example.com",
            password_hash="hash",
            joined_date="2026-04-10",
            total_habits=0,
            current_streak=0
        )
        db.add(new_user)
        db.commit()
        print(f"User created: {user_id}")

        # 2. Try creating a habit
        habit_id = str(uuid.uuid4())
        try:
            new_habit = Habit(
                id=habit_id,
                user_id=user_id,
                habit_name="Test Habit",
                category="health",
                goal_days=30,
                target_per_day=1,
                start_date="2026-04-10",
                reminder_time="07:00",
                color_theme="green",
                days_of_week="1,2,3,4,5,6,7",
                created_at=datetime.now().isoformat(),
                current_streak=0,
                longest_streak=0,
                progress_percentage=0,
                completed_days_count=0
            )
            db.add(new_habit)
            db.commit()
            print(f"Habit created: {habit_id}")
        except Exception as e:
            db.rollback()
            print(f"Error creating Habit: {e}")

        # 3. Try creating a goal
        goal_id = str(uuid.uuid4())
        try:
            new_goal = Goal(
                id=goal_id,
                user_id=user_id,
                goal_name="Test Goal",
                target_value=100,
                actual_value=0,
                deadline="2026-05-10",
                status_percentage=0,
                days_of_week="1,2,3,4,5,6,7",
                created_at=datetime.now().isoformat()
            )
            db.add(new_goal)
            db.commit()
            print(f"Goal created: {goal_id}")
        except Exception as e:
            db.rollback()
            print(f"Error creating Goal: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    test_creation()
