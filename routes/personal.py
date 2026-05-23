from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db, User, CalorieLog, PeriodLog
from schemas.personal import (
    CalorieLogCreate, CalorieLogResponse, DailyCalorieSummary,
    PeriodLogCreate, PeriodLogResponse, PeriodPrediction, PersonalProfileUpdate
)
from utils.dependencies import get_current_user
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/profile/personal", tags=["Personal Tracking"])

@router.get("", response_model=PersonalProfileUpdate)
async def get_personal_profile(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("", response_model=dict)
async def update_personal_profile(data: PersonalProfileUpdate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if data.gender is not None: user.gender = data.gender
    if data.height is not None: user.height = data.height
    if data.weight is not None: user.weight = data.weight
    if data.daily_calorie_goal is not None: user.daily_calorie_goal = data.daily_calorie_goal
    if data.step_goal is not None: user.step_goal = data.step_goal
    
    db.commit()
    return {"message": "Personal profile updated successfully"}

# -- Calorie Endpoints --
calorie_router = APIRouter(prefix="/calories", tags=["Calorie Tracking"])

@calorie_router.post("", response_model=CalorieLogResponse)
async def log_calories(log: CalorieLogCreate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now()
    new_log = CalorieLog(
        user_id=uid,
        food_name=log.food_name,
        calories=log.calories,
        date=now.strftime("%Y-%m-%d"),
        timestamp=now.isoformat()
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@calorie_router.get("/today", response_model=DailyCalorieSummary)
async def get_today_calories(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    logs = db.query(CalorieLog).filter(CalorieLog.user_id == uid, CalorieLog.date == today).all()
    user = db.query(User).filter(User.id == uid).first()
    
    total = sum(item.calories for item in logs)
    return DailyCalorieSummary(
        total_calories=total,
        daily_goal=user.daily_calorie_goal if user else 2000,
        logs=logs
    )

@calorie_router.delete("/{log_id}")
async def delete_calorie_log(log_id: int, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    log = db.query(CalorieLog).filter(CalorieLog.id == log_id, CalorieLog.user_id == uid).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    db.delete(log)
    db.commit()
    return {"message": "Deleted successfully"}

# -- Period Endpoints --
period_router = APIRouter(prefix="/periods", tags=["Period Tracking"])

@period_router.post("", response_model=PeriodLogResponse)
async def log_period(log: PeriodLogCreate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # Simple check if current status is female
    user = db.query(User).filter(User.id == uid).first()
    if user.gender != "female":
        raise HTTPException(status_code=403, detail="Period tracking only available for female users")

    new_log = PeriodLog(
        user_id=uid,
        start_date=log.start_date,
        end_date=log.end_date,
        cycle_length=log.cycle_length,
        symptoms=json.dumps(log.symptoms) if log.symptoms else None
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@period_router.get("/history", response_model=List[PeriodLogResponse])
async def get_period_history(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    logs = db.query(PeriodLog).filter(PeriodLog.user_id == uid).order_by(PeriodLog.start_date.desc()).limit(3).all()
    return logs

@period_router.get("/prediction", response_model=PeriodPrediction)
async def get_period_prediction(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    last_period = db.query(PeriodLog).filter(PeriodLog.user_id == uid).order_by(PeriodLog.start_date.desc()).first()
    
    if not last_period:
        return PeriodPrediction(
            next_period_date="Not enough data",
            ovulation_day="Not enough data",
            status_message="Log your first period to see predictions"
        )
    
    start_dt = datetime.strptime(last_period.start_date, "%Y-%m-%d")
    cycle_days = last_period.cycle_length or 28
    
    next_start = start_dt + timedelta(days=cycle_days)
    ovulation = start_dt + timedelta(days=cycle_days - 14)
    
    today = datetime.now()
    days_until = (next_start - today).days
    
    if days_until < 0:
        msg = f"Period started {abs(days_until)} days ago"
    elif days_until == 0:
        msg = "Period expected today"
    else:
        msg = f"Period expected in {days_until} days"
        
    return PeriodPrediction(
        next_period_date=next_start.strftime("%Y-%m-%d"),
        ovulation_day=ovulation.strftime("%Y-%m-%d"),
        status_message=msg
    )
