import os
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Float, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, index=True) # UUID
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    joined_date = Column(String(10)) # YYYY-MM-DD
    total_habits = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    
    # Personal health fields
    gender = Column(String(10), nullable=True)          # 'male' or 'female'
    height = Column(Float, nullable=True)               # cm
    weight = Column(Float, nullable=True)               # kg
    daily_calorie_goal = Column(Integer, default=2000)
    daily_protein_goal = Column(Float, default=50.0)
    water_goal_glasses = Column(Integer, default=8)
    diet_type = Column(String(20), default="Veg")      # 'Veg', 'Non-Veg', 'Vegan'
    allergies = Column(String(255), nullable=True)      # Comma separated
    step_goal = Column(Integer, default=10000)
    scan_credits = Column(Integer, default=3)
    
    habits = relationship("Habit", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    calorie_logs = relationship("CalorieLog", back_populates="user", cascade="all, delete-orphan")
    food_logs = relationship("FoodLog", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    water_logs = relationship("WaterLog", back_populates="user", cascade="all, delete-orphan")
    period_logs = relationship("PeriodLog", back_populates="user", cascade="all, delete-orphan")

class Habit(Base):
    __tablename__ = "habits"
    id = Column(String(36), primary_key=True, index=True) # UUID
    user_id = Column(String(36), ForeignKey("users.id"))
    habit_name = Column(String(100))
    category = Column(String(50))
    goal_days = Column(Integer)
    target_per_day = Column(Integer, default=1)
    start_date = Column(String(10)) # YYYY-MM-DD
    reminder_time = Column(String(10)) # HH:MM
    color_theme = Column(String(20))
    created_at = Column(String(30)) # ISO format
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    progress_percentage = Column(Integer, default=0)
    completed_days_count = Column(Integer, default=0)
    days_of_week = Column(String(50), default="1,2,3,4,5,6,7") # 1=Mon, ..., 7=Sun


    owner = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    habit_id = Column(String(36), ForeignKey("habits.id"))
    date = Column(String(10), index=True) # YYYY-MM-DD
    status = Column(Boolean, default=False)
    timestamp = Column(String(30)) # ISO format

    habit = relationship("Habit", back_populates="logs")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(String(36), primary_key=True, index=True) # UUID
    user_id = Column(String(36), ForeignKey("users.id"))
    goal_name = Column(String(100))
    target_value = Column(Integer)
    actual_value = Column(Integer, default=0)
    deadline = Column(String(10)) # YYYY-MM-DD
    status_percentage = Column(Integer, default=0)
    days_of_week = Column(String(50), default="1,2,3,4,5,6,7") # 1=Mon, ..., 7=Sun

    created_at = Column(String(30)) # ISO format

    owner = relationship("User", back_populates="goals")

class CalorieLog(Base):
    __tablename__ = "calorie_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    food_name = Column(String(150))
    calories = Column(Integer)
    date = Column(String(10), index=True)  # YYYY-MM-DD
    timestamp = Column(String(30))         # ISO format

    user = relationship("User", back_populates="calorie_logs")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), index=True)
    emoji = Column(String(10))
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    diet_type = Column(String(20)) # Veg, Non-Veg, Vegan
    meal_type = Column(String(20)) # Breakfast, Lunch, Dinner, Snack
    serving_size = Column(String(50))

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food_name = Column(String(150), unique=True, index=True)
    prep_time = Column(String(20))
    cook_time = Column(String(20))
    difficulty = Column(String(20)) # Easy, Medium, Hard
    servings = Column(Integer)
    ingredients = Column(Text) # JSON string
    instructions = Column(Text) # JSON string
    tips = Column(Text) # JSON string

class FoodLog(Base):
    __tablename__ = "food_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    food_name = Column(String(150))
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    meal_type = Column(String(20)) # breakfast, lunch, dinner, snack
    portion_size = Column(String(20)) # small, medium, large
    date = Column(String(10), index=True)  # YYYY-MM-DD
    timestamp = Column(String(30))         # ISO format

    user = relationship("User", back_populates="food_logs")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    week_start_date = Column(String(10), index=True) # YYYY-MM-DD
    day_of_week = Column(String(10)) # Monday, Tuesday, ...
    meal_type = Column(String(20))
    food_name = Column(String(150))
    calories = Column(Integer)
    diet_type = Column(String(20))

    user = relationship("User", back_populates="meal_plans")

class WaterLog(Base):
    __tablename__ = "water_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    glasses = Column(Integer, default=1)
    date = Column(String(10), index=True) # YYYY-MM-DD
    timestamp = Column(String(30))

    user = relationship("User", back_populates="water_logs")

class PeriodLog(Base):
    __tablename__ = "period_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    start_date = Column(String(10))   # YYYY-MM-DD
    end_date = Column(String(10), nullable=True)  # YYYY-MM-DD
    cycle_length = Column(Integer, default=28)
    symptoms = Column(Text, nullable=True)  # JSON-encoded list of strings

    user = relationship("User", back_populates="period_logs")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
