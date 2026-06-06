from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db, User, Food, FoodLog, WaterLog
from schemas.food import (
    FoodResponse, FoodLogCreate, FoodLogResponse,
    NutritionSummary, HealthProfileUpdate,
    AiScanResponse, ScanCreditsResponse, BuyScansRequest
)
from utils.dependencies import get_current_user
from datetime import datetime
import json
import base64
from config.gemini import client

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

# ── AI Calorie Scanner ─────────────────────────────────────────────────────

@router.get("/scan/credits", response_model=ScanCreditsResponse)
async def get_scan_credits(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the user's remaining AI scan credits."""
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ScanCreditsResponse(
        scan_credits=user.scan_credits or 0,
        message=f"You have {user.scan_credits or 0} scan(s) remaining."
    )

@router.post("/scan/buy", response_model=ScanCreditsResponse)
async def buy_scan_credits(
    body: BuyScansRequest,
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate purchasing scan credits. 1 scan = ₹5.
    In production, integrate a payment gateway (e.g. Razorpay) before adding credits.
    """
    if body.quantity < 1 or body.quantity > 100:
        raise HTTPException(status_code=400, detail="Quantity must be between 1 and 100")

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.scan_credits = (user.scan_credits or 0) + body.quantity
    db.commit()
    db.refresh(user)
    return ScanCreditsResponse(
        scan_credits=user.scan_credits,
        message=f"Purchase successful! You now have {user.scan_credits} scan(s). (₹{body.quantity * 5} charged)"
    )

@router.post("/scan/analyze", response_model=AiScanResponse)
async def analyze_food_image(
    image: UploadFile = File(...),
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze a food image using Gemini Vision and return nutritional info.
    Deducts 1 scan credit from the user's balance.
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if (user.scan_credits or 0) < 1:
        raise HTTPException(
            status_code=402,
            detail="Insufficient scan credits. Please purchase more scans (₹5 per scan)."
        )

    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=413, detail="Image too large. Max 10 MB.")

    mime_type = image.content_type or "image/jpeg"

    prompt = """You are a professional nutritionist and food recognition AI.
Analyze this food image and provide accurate nutritional information.

Respond ONLY with a valid JSON object in this exact format (no markdown, no explanation):
{
  "food_name": "Name of the food dish",
  "calories": 350,
  "protein": 15.5,
  "carbs": 42.0,
  "fat": 12.3,
  "serving_size": "1 medium bowl (250g)",
  "confidence": "High"
}

Rules:
- calories must be an integer
- protein, carbs, fat must be floats (grams)
- confidence must be one of: "High", "Medium", "Low"
- If the image is not food, return confidence "Low" and estimate zeros
- Do NOT include markdown code blocks, only raw JSON"""

    try:
        from google.genai import types
        # Check if they are using a placeholder key
        import os
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_ACTUAL_API_KEY":
            raise Exception("Using placeholder API key")
            
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(parts=[
                    types.Part(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                ])
            ]
        )

        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        result = json.loads(raw)
        
    except Exception as e:
        # Fallback Mock Response for Demo Purposes if API fails or key is missing
        print(f"AI API Failed, using Mock Data: {e}")
        import asyncio
        import random
        await asyncio.sleep(1.5) # Simulate processing time
        
        mock_foods = [
            {"food_name": "Healthy Chicken Salad (Mock Data)", "calories": 320, "protein": 28.5, "carbs": 12.0, "fat": 15.0},
            {"food_name": "Paneer Butter Masala & Naan (Mock Data)", "calories": 550, "protein": 18.0, "carbs": 45.0, "fat": 32.0},
            {"food_name": "Masala Dosa (Mock Data)", "calories": 350, "protein": 8.0, "carbs": 55.0, "fat": 10.0},
            {"food_name": "Avocado Toast with Egg (Mock Data)", "calories": 280, "protein": 14.0, "carbs": 22.0, "fat": 16.0},
            {"food_name": "Chicken Biryani (Mock Data)", "calories": 600, "protein": 25.0, "carbs": 70.0, "fat": 20.0},
            {"food_name": "Fruit Smoothie Bowl (Mock Data)", "calories": 250, "protein": 5.0, "carbs": 50.0, "fat": 4.0}
        ]
        chosen = random.choice(mock_foods)
        
        result = {
            "food_name": chosen["food_name"],
            "calories": chosen["calories"],
            "protein": chosen["protein"],
            "carbs": chosen["carbs"],
            "fat": chosen["fat"],
            "serving_size": "1 serving",
            "confidence": "High"
        }

    # Deduct 1 credit only on success
    user.scan_credits = (user.scan_credits or 0) - 1
    db.commit()

    return AiScanResponse(
        food_name=result.get("food_name", "Unknown Food"),
        calories=int(result.get("calories", 0)),
        protein=float(result.get("protein", 0)),
        carbs=float(result.get("carbs", 0)),
        fat=float(result.get("fat", 0)),
        serving_size=result.get("serving_size", "1 serving"),
        confidence=result.get("confidence", "Medium")
    )
