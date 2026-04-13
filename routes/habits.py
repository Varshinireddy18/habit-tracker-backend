from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.habits import HabitCreate, HabitUpdate, HabitResponse, HabitLogRequest, HabitLogEntry, HabitMonthResponse
from config.database import get_db, Habit, HabitLog, User
from utils.dependencies import get_current_user
from services.habit_service import HabitService
from datetime import datetime
import uuid

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("", response_model=dict)
async def create_habit(habit: HabitCreate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        habit_id = str(uuid.uuid4())
        habit_data = habit.dict()
        
        new_habit = Habit(
            id=habit_id,
            user_id=uid,
            **habit_data,
            created_at=datetime.now().isoformat(),
            current_streak=0,
            longest_streak=0,
            progress_percentage=0,
            completed_days_count=0
        )
        
        db.add(new_habit)
        
        # Increment total_habits in user profile
        user = db.query(User).filter(User.id == uid).first()
        if user:
            user.total_habits += 1
            
        db.commit()
        
        return {"message": "Habit created successfully", "habit_id": habit_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[HabitResponse])
async def get_habits(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        habits = db.query(Habit).filter(Habit.user_id == uid).all()
        today = datetime.now().strftime("%Y-%m-%d")
        response = []
        
        for habit in habits:
            # Check if completed today
            log = db.query(HabitLog).filter(
                HabitLog.user_id == uid, 
                HabitLog.habit_id == habit.id, 
                HabitLog.date == today
            ).first()
            
            completed_today = log is not None and log.status == True
            
            response.append(HabitResponse(
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
                completed_today=completed_today
            ))
            
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(habit_id: str, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == uid).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
        
    today = datetime.now().strftime("%Y-%m-%d")
    log = db.query(HabitLog).filter(
        HabitLog.user_id == uid, 
        HabitLog.habit_id == habit_id, 
        HabitLog.date == today
    ).first()
    
    completed_today = log is not None and log.status == True
    
    return HabitResponse(
        id=habit_id,
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
        completed_today=completed_today
    )

@router.put("/{habit_id}", response_model=dict)
async def update_habit(habit_id: str, habit: HabitUpdate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == uid).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
        
    for var, value in habit.dict().items():
        if value is not None:
            setattr(db_habit, var, value)
            
    db.commit()
    
    # Re-calculate stats only if goal_days changed
    if habit.goal_days is not None:
        HabitService.update_habit_stats(db, uid, habit_id)
        
    return {"message": "Habit updated successfully"}

@router.delete("/{habit_id}", response_model=dict)
async def delete_habit(habit_id: str, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == uid).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
        
    db.delete(db_habit)
    
    # Decrement total_habits
    user = db.query(User).filter(User.id == uid).first()
    if user:
        user.total_habits -= 1
        
    db.commit()
    return {"message": "Habit deleted successfully"}

@router.post("/{habit_id}/mark-complete", response_model=dict)
async def mark_complete(habit_id: str, log_req: HabitLogRequest, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # ... logic stays same ...
    log = db.query(HabitLog).filter(
        HabitLog.user_id == uid, 
        HabitLog.habit_id == habit_id, 
        HabitLog.date == log_req.date
    ).first()
    
    if log:
        log.status = log_req.status
        log.timestamp = datetime.now().isoformat()
    else:
        log = HabitLog(
            user_id=uid,
            habit_id=habit_id,
            date=log_req.date,
            status=log_req.status,
            timestamp=datetime.now().isoformat()
        )
        db.add(log)
    
    db.commit()
    HabitService.update_habit_stats(db, uid, habit_id)
    return {"message": f"Habit marked as {'complete' if log_req.status else 'incomplete'}"}

@router.get("/logs/monthly", response_model=list[HabitMonthResponse])
async def get_monthly_logs(month: str, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Fetch logs for all habits for a specific month (YYYY-MM).
    """
    try:
        # Get all habits for user
        habits = db.query(Habit).filter(Habit.user_id == uid).all()
        month_prefix = f"{month}-%"
        
        response = []
        for habit in habits:
            habit_logs = db.query(HabitLog).filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == uid,
                HabitLog.date.like(month_prefix)
            ).all()
            
            response.append(HabitMonthResponse(
                habit_id=habit.id,
                logs=[HabitLogEntry(date=l.date, status=l.status) for l in habit_logs]
            ))
            
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
