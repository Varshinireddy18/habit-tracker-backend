from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.dashboard import WeeklyAnalytics, MonthlyAnalytics
from config.database import get_db, Habit, HabitLog
from utils.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/weekly", response_model=WeeklyAnalytics)
async def get_weekly_analytics(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        weekly_stats = {}
        
        total_habits = db.query(Habit).filter(Habit.user_id == uid).count()
        
        if total_habits == 0:
            return WeeklyAnalytics(**{day: 0 for day in days_of_week})
            
        # Get logs for the entire week in one go
        start_date_str = start_of_week.strftime("%Y-%m-%d")
        end_date_str = (start_of_week + timedelta(days=6)).strftime("%Y-%m-%d")
        
        logs = db.query(
            HabitLog.date, 
            func.count(HabitLog.id).label("count")
        ).filter(
            HabitLog.user_id == uid,
            HabitLog.status == True,
            HabitLog.date >= start_date_str,
            HabitLog.date <= end_date_str
        ).group_by(HabitLog.date).all()
        
        log_counts = {log.date: log.count for log in logs}
        
        for i, day_name in enumerate(days_of_week):
            check_date = (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d")
            completed_count = log_counts.get(check_date, 0)
            weekly_stats[day_name] = int(round((completed_count / total_habits) * 100))
            
        return WeeklyAnalytics(**weekly_stats)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/monthly", response_model=MonthlyAnalytics)
async def get_monthly_analytics(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        today = datetime.now()
        monthly_progress = []
        
        total_habits = db.query(Habit).filter(Habit.user_id == uid).count()
        
        if total_habits == 0:
            return MonthlyAnalytics(progress=[0]*30)
            
        # Get logs for the last 30 days in one go
        start_date_str = (today - timedelta(days=29)).strftime("%Y-%m-%d")
        
        logs = db.query(
            HabitLog.date, 
            func.count(HabitLog.id).label("count")
        ).filter(
            HabitLog.user_id == uid,
            HabitLog.status == True,
            HabitLog.date >= start_date_str
        ).group_by(HabitLog.date).all()
        
        log_counts = {log.date: log.count for log in logs}
            
        for i in range(30):
            check_date = (today - timedelta(days=29-i)).strftime("%Y-%m-%d")
            completed_count = log_counts.get(check_date, 0)
            monthly_progress.append(int(round((completed_count / total_habits) * 100)))
            
        return MonthlyAnalytics(progress=monthly_progress)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
