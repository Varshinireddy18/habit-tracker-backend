from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db, User, Food, MealPlan
from schemas.food import WeeklyMealPlanResponse, DailyMealPlan, MealPlanItem
from utils.dependencies import get_current_user
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/meal-plan", tags=["Meal Planning"])

@router.get("/generate", response_model=WeeklyMealPlanResponse)
async def generate_meal_plan(
    diet: str = Query(..., pattern="^(Veg|Non-Veg|Vegan)$"),
    goal: str = Query(..., pattern="^(Weight Loss|Maintain Weight|Weight Gain)$"),
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == uid).first()
    target_cal = user.daily_calorie_goal
    
    # Adjust target based on goal
    if goal == "Weight Loss":
        target_cal -= 500
    elif goal == "Weight Gain":
        target_cal += 500
        
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_plan = []
    
    # Fetch available foods based on diet
    def get_foods(m_type):
        q = db.query(Food).filter(Food.meal_type == m_type)
        if diet == "Veg":
            q = q.filter(Food.diet_type.in_(["Veg", "Vegan"]))
        elif diet == "Vegan":
            q = q.filter(Food.diet_type == "Vegan")
        return q.all()

    breakfasts = get_foods("Breakfast")
    lunches = get_foods("Lunch")
    dinners = get_foods("Dinner")
    snacks = get_foods("Snack")

    if not (breakfasts and lunches and dinners and snacks):
        raise HTTPException(status_code=400, detail="Not enough food data to generate plan")

    start_date = datetime.now().strftime("%Y-%m-%d")
    
    # Clear old plan for this week
    db.query(MealPlan).filter(MealPlan.user_id == uid).delete()

    for day in days:
        # Simple random selection for now, could be more complex (AI-powered)
        b = random.choice(breakfasts)
        l = random.choice(lunches)
        d = random.choice(dinners)
        s1 = random.choice(snacks)
        s2 = random.choice([s for s in snacks if s.id != s1.id])
        
        day_meals = [
            MealPlanItem(meal_type="Breakfast", food_name=b.name, calories=b.calories, emoji=b.emoji),
            MealPlanItem(meal_type="Lunch", food_name=l.name, calories=l.calories, emoji=l.emoji),
            MealPlanItem(meal_type="Dinner", food_name=d.name, calories=d.calories, emoji=d.emoji),
            MealPlanItem(meal_type="Snack 1", food_name=s1.name, calories=s1.calories, emoji=s1.emoji),
            MealPlanItem(meal_type="Snack 2", food_name=s2.name, calories=s2.calories, emoji=s2.emoji),
        ]
        
        total_day_cal = sum(m.calories for m in day_meals)
        weekly_plan.append(DailyMealPlan(day=day, meals=day_meals, total_calories=total_day_cal))
        
        # Save to DB
        for m in day_meals:
            db.add(MealPlan(
                user_id=uid,
                week_start_date=start_date,
                day_of_week=day,
                meal_type=m.meal_type,
                food_name=m.food_name,
                calories=m.calories,
                diet_type=diet
            ))
            
    db.commit()
    return WeeklyMealPlanResponse(week_start_date=start_date, days=weekly_plan)

@router.get("/current", response_model=WeeklyMealPlanResponse)
async def get_current_meal_plan(
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch most recent plan
    latest = db.query(MealPlan).filter(MealPlan.user_id == uid).order_by(MealPlan.id.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No meal plan found")
        
    start_date = latest.week_start_date
    logs = db.query(MealPlan).filter(MealPlan.user_id == uid, MealPlan.week_start_date == start_date).all()
    
    days_data = {}
    for log in logs:
        if log.day_of_week not in days_data:
            days_data[log.day_of_week] = []
        
        # Get emoji from Food table
        food_item = db.query(Food).filter(Food.name == log.food_name).first()
        emoji = food_item.emoji if food_item else "🍽️"
        
        days_data[log.day_of_week].append(MealPlanItem(
            meal_type=log.meal_type,
            food_name=log.food_name,
            calories=log.calories,
            emoji=emoji
        ))
        
    response_days = []
    for day, meals in days_data.items():
        response_days.append(DailyMealPlan(
            day=day,
            meals=meals,
            total_calories=sum(m.calories for m in meals)
        ))
        
    return WeeklyMealPlanResponse(week_start_date=start_date, days=response_days)
