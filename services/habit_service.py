from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from config.database import Habit, HabitLog, User

class HabitService:
    @staticmethod
    def calculate_progress(completed_days: int, goal_days: int) -> int:
        if goal_days <= 0:
            return 0
        progress = (completed_days / goal_days) * 100
        return int(round(progress))

    @staticmethod
    def get_habit_logs(db: Session, user_id: str, habit_id: str):
        logs = db.query(HabitLog).filter(
            HabitLog.user_id == user_id, 
            HabitLog.habit_id == habit_id
        ).all()
        return {log.date: {"status": log.status} for log in logs}

    @staticmethod
    def calculate_streaks(db: Session, user_id: str, habit_id: str):
        logs = db.query(HabitLog).filter(
            HabitLog.user_id == user_id,
            HabitLog.habit_id == habit_id,
            HabitLog.status == True
        ).order_by(desc(HabitLog.date)).all()
        
        if not logs:
            return 0, 0 # current, longest

        completed_dates = [log.date for log in logs]
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        check_date = today
        # If not completed today, check from yesterday
        if today.isoformat() not in completed_dates:
            check_date = yesterday
        
        for i in range(len(completed_dates)):
            date_str = check_date.isoformat()
            if date_str in completed_dates:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Calculate longest streak
        all_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in completed_dates])
        longest_streak = 0
        temp_streak = 0
        if all_dates:
            temp_streak = 1
            longest_streak = 1
            for i in range(1, len(all_dates)):
                if all_dates[i] == all_dates[i-1] + timedelta(days=1):
                    temp_streak += 1
                else:
                    temp_streak = 1
                longest_streak = max(longest_streak, temp_streak)

        return current_streak, longest_streak

    @staticmethod
    def update_habit_stats(db: Session, user_id: str, habit_id: str):
        current_streak, longest_streak = HabitService.calculate_streaks(db, user_id, habit_id)
        
        completed_days_count = db.query(HabitLog).filter(
            HabitLog.user_id == user_id,
            HabitLog.habit_id == habit_id,
            HabitLog.status == True
        ).count()
        
        habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()
        if habit:
            goal_days = habit.goal_days or 30
            progress = HabitService.calculate_progress(completed_days_count, goal_days)
            
            habit.current_streak = current_streak
            habit.longest_streak = longest_streak
            habit.progress_percentage = progress
            habit.completed_days_count = completed_days_count
            
            db.commit()
            return True
        return False
