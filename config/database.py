import os
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Float, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "habit_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
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
    
    habits = relationship("Habit", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")

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
