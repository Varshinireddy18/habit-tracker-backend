from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FoodBase(BaseModel):
    name: str
    emoji: str
    calories: int
    protein: float
    carbs: float
    fat: float
    diet_type: str
    meal_type: str
    serving_size: str

class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True

class FoodLogCreate(BaseModel):
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    meal_type: str
    portion_size: str # small, medium, large

class FoodLogResponse(BaseModel):
    id: int
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    meal_type: str
    portion_size: str
    date: str
    timestamp: str

    class Config:
        from_attributes = True

class NutritionSummary(BaseModel):
    total_calories: int
    calorie_goal: int
    total_protein: float
    protein_goal: float
    total_carbs: float
    total_fat: float
    total_fiber: float # Placeholder
    water_glasses: int
    water_goal: int
    logs: List[FoodLogResponse]

class RecipeResponse(BaseModel):
    food_name: str
    prep_time: str
    cook_time: str
    difficulty: str
    servings: int
    ingredients: List[str]
    instructions: List[str]
    tips: List[str]

    class Config:
        from_attributes = True

class MealPlanItem(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    emoji: Optional[str] = "🍽️"

class DailyMealPlan(BaseModel):
    day: str
    meals: List[MealPlanItem]
    total_calories: int

class WeeklyMealPlanResponse(BaseModel):
    week_start_date: str
    days: List[DailyMealPlan]

class MealPlanGenerateRequest(BaseModel):
    diet_type: str
    goal: str # Weight Loss, Maintain, Weight Gain
    allergies: Optional[str] = "None"

class HealthProfileUpdate(BaseModel):
    diet_type: Optional[str] = None
    daily_calorie_goal: Optional[int] = None
    daily_protein_goal: Optional[float] = None
    water_goal_glasses: Optional[int] = None
    allergies: Optional[str] = None

class AiScanResponse(BaseModel):
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    serving_size: str
    confidence: str  # e.g. "High", "Medium", "Low"

class ScanCreditsResponse(BaseModel):
    scan_credits: int
    message: str

class BuyScansRequest(BaseModel):
    quantity: int = 1  # number of scans to buy (1 scan = ₹5)
