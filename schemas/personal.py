from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CalorieLogCreate(BaseModel):
    food_name: str
    calories: int

class CalorieLogResponse(BaseModel):
    id: int
    food_name: str
    calories: int
    date: str
    timestamp: str

    class Config:
        from_attributes = True

class DailyCalorieSummary(BaseModel):
    total_calories: int
    daily_goal: int
    logs: List[CalorieLogResponse]

class PeriodLogCreate(BaseModel):
    start_date: str
    end_date: Optional[str] = None
    cycle_length: int = 28
    symptoms: Optional[List[str]] = []

class PeriodLogResponse(BaseModel):
    id: int
    start_date: str
    end_date: Optional[str] = None
    cycle_length: int
    symptoms: Optional[str] = None # JSON string or comma separated

    class Config:
        from_attributes = True

class PeriodPrediction(BaseModel):
    next_period_date: str
    ovulation_day: str
    status_message: str

class PersonalProfileUpdate(BaseModel):
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    daily_calorie_goal: Optional[int] = None
    step_goal: Optional[int] = None
