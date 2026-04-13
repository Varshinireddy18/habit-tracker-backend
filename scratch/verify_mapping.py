
import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Habit, Goal, User
from schemas.habits import HabitResponse
from schemas.goals import GoalResponse
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

def verify_response_mapping():
    db = SessionLocal()
    try:
        # 1. Test Habit mapping
        habit = db.query(Habit).first()
        if habit:
            print(f"Testing HabitResponse mapping for habit: {habit.habit_name}")
            try:
                resp = HabitResponse(
                    id=habit.id,
                    habit_name=habit.habit_name,
                    category=habit.category,
                    goal_days=habit.goal_days,
                    target_per_day=habit.target_per_day,
                    start_date=habit.start_date,
                    reminder_time=habit.reminder_time,
                    color_theme=habit.color_theme,
                    days_of_week=habit.days_of_week,
                    progress=habit.progress_percentage or 0,
                    streak=habit.current_streak or 0,
                    completed_today=False
                )
                print("HabitResponse mapping SUCCESS")
            except Exception as e:
                print(f"HabitResponse mapping FAILED: {e}")
        else:
            print("No habits found to test.")

        # 2. Test Goal mapping
        goal = db.query(Goal).first()
        if goal:
            print(f"\nTesting GoalResponse mapping for goal: {goal.goal_name}")
            try:
                resp = GoalResponse(
                    id=goal.id,
                    goal_name=goal.goal_name,
                    target_value=goal.target_value,
                    actual_value=goal.actual_value,
                    deadline=goal.deadline,
                    status_percentage=goal.status_percentage,
                    days_of_week=goal.days_of_week
                )
                print("GoalResponse mapping SUCCESS")
            except Exception as e:
                print(f"GoalResponse mapping FAILED: {e}")
        else:
            print("No goals found to test.")

    finally:
        db.close()

if __name__ == "__main__":
    verify_response_mapping()
