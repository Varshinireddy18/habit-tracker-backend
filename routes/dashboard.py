from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.dashboard import DashboardResponse, DonutChartData
from config.database import get_db, Habit, HabitLog
from utils.dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Total Habits
        total_habits = db.query(Habit).filter(Habit.user_id == uid).count()
        
        if total_habits == 0:
            return DashboardResponse(
                total_habits=0,
                completed_today=0,
                pending_today=0,
                overall_progress=0,
                current_streak=0,
                weekly_progress=[0, 0, 0, 0],
                monthly_progress=0
            )

        # 2. Completed Today
        completed_today = db.query(HabitLog).filter(
            HabitLog.user_id == uid,
            HabitLog.date == today,
            HabitLog.status == True
        ).count()
        
        # 3. Progress & Streaks
        stats = db.query(
            func.sum(Habit.progress_percentage).label("total_progress"),
            func.max(Habit.current_streak).label("max_streak")
        ).filter(Habit.user_id == uid).first()
        
        total_progress = stats.total_progress or 0
        current_streak = stats.max_streak or 0
        
        pending_today = total_habits - completed_today
        overall_progress = int(round(total_progress / total_habits))
        
        # 4. Weekly Progress (Maintaining original mock data as requested by UI requirements)
        weekly_progress = [70, 80, 90, 100]
        
        return DashboardResponse(
            total_habits=total_habits,
            completed_today=completed_today,
            pending_today=pending_today,
            overall_progress=overall_progress,
            current_streak=current_streak,
            weekly_progress=weekly_progress,
            monthly_progress=overall_progress
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/chart-data", response_model=DonutChartData)
async def get_chart_data(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    
    total_habits = db.query(Habit).filter(Habit.user_id == uid).count()
    
    if total_habits == 0:
        return DonutChartData(completed=0, remaining=100)
    
    completed_today = db.query(HabitLog).filter(
        HabitLog.user_id == uid,
        HabitLog.date == today,
        HabitLog.status == True
    ).count()
    
    completed_percentage = int(round((completed_today / total_habits) * 100))
    return DonutChartData(completed=completed_percentage, remaining=100 - completed_percentage)
