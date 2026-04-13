from pydantic import BaseModel
from typing import List, Dict

class DashboardResponse(BaseModel):
    total_habits: int
    completed_today: int
    pending_today: int
    overall_progress: int
    current_streak: int
    weekly_progress: List[int]
    monthly_progress: int

class DonutChartData(BaseModel):
    completed: int
    remaining: int

class WeeklyAnalytics(BaseModel):
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int

class MonthlyAnalytics(BaseModel):
    progress: List[int] # 30-day progress array
