from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db, User, Food, FoodLog, WaterLog
from schemas.food import (
    FoodResponse, FoodLogCreate, FoodLogResponse, 
    NutritionSummary, HealthProfileUpdate
)
from utils.dependencies import get_current_user
from datetime import datetime
import json

router = APIRouter(prefix="/food", tags=["Food Tracking"])

@router.get("/search", response_model=List[FoodResponse])
async def search_food(
    q: str = Query(..., min_length=1),
    diet: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Food).filter(Food.name.ilike(f"%{q}%"))
    if diet:
        # If diet is Veg, include Vegan too. If Vegan, only Vegan.
        if diet == "Veg":
            query = query.filter(Food.diet_type.in_(["Veg", "Vegan"]))
        elif diet == "Vegan":
            query = query.filter(Food.diet_type == "Vegan")
        elif diet == "Non-Veg":
            pass # Non-Veg can eat everything
            
    return query.limit(20).all()

@router.get("/suggestions", response_model=List[FoodResponse])
async def get_suggestions(
    remaining_cal: int,
    diet: str,
    db: Session = Depends(get_db)
):
    from sqlalchemy.sql.expression import func
    # Suggest foods that are within remaining calories
    query = db.query(Food).filter(Food.calories <= remaining_cal)
    
    if diet == "Veg":
        query = query.filter(Food.diet_type.in_(["Veg", "Vegan"]))
    elif diet == "Vegan":
        query = query.filter(Food.diet_type == "Vegan")
        
    # Return a randomized mix of 15 suggestions for variety
    return query.order_by(func.random()).limit(15).all()

@router.post("/log", response_model=FoodLogResponse)
async def log_food(
    log: FoodLogCreate,
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    new_log = FoodLog(
        user_id=uid,
        food_name=log.food_name,
        calories=log.calories,
        protein=log.protein,
        carbs=log.carbs,
        fat=log.fat,
        meal_type=log.meal_type,
        portion_size=log.portion_size,
        date=now.strftime("%Y-%m-%d"),
        timestamp=now.isoformat()
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/today", response_model=List[FoodLogResponse])
async def get_today_food(
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = datetime.now().strftime("%Y-%m-%d")
    return db.query(FoodLog).filter(FoodLog.user_id == uid, FoodLog.date == today).all()

@router.get("/nutrition/today", response_model=NutritionSummary)
async def get_nutrition_summary(
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = datetime.now().strftime("%Y-%m-%d")
    logs = db.query(FoodLog).filter(FoodLog.user_id == uid, FoodLog.date == today).all()
    user = db.query(User).filter(User.id == uid).first()
    
    water_logs = db.query(WaterLog).filter(WaterLog.user_id == uid, WaterLog.date == today).all()
    total_water = sum(w.glasses for w in water_logs)
    
    total_cal = sum(log.calories for log in logs)
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)
    total_fat = sum(log.fat for log in logs)
    
    return NutritionSummary(
        total_calories=total_cal,
        calorie_goal=user.daily_calorie_goal,
        total_protein=total_protein,
        protein_goal=user.daily_protein_goal,
        total_carbs=total_carbs,
        total_fat=total_fat,
        total_fiber=0.0, # Placeholder
        water_glasses=total_water,
        water_goal=user.water_goal_glasses,
        logs=logs
    )

@router.post("/water/log", response_model=dict)
async def log_water(
    glasses: int = Query(1),
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = datetime.now().strftime("%Y-%m-%d")
    new_log = WaterLog(
        user_id=uid,
        glasses=glasses,
        date=today,
        timestamp=datetime.now().isoformat()
    )
    db.add(new_log)
    db.commit()
    return {"message": "Water logged", "total_today": glasses}

@router.put("/profile/health", response_model=dict)
async def update_health_profile(
    data: HealthProfileUpdate,
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if data.diet_type: user.diet_type = data.diet_type
    if data.daily_calorie_goal: user.daily_calorie_goal = data.daily_calorie_goal
    if data.daily_protein_goal: user.daily_protein_goal = data.daily_protein_goal
    if data.water_goal_glasses: user.water_goal_glasses = data.water_goal_glasses
    if data.allergies: user.allergies = data.allergies
    
    db.commit()
    return {"message": "Health profile updated"}
