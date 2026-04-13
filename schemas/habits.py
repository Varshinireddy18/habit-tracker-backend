from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class HabitBase(BaseModel):
    habit_name: str
    category: str
    goal_days: int = Field(..., gt=0)
    target_per_day: int = Field(1, gt=0)
    start_date: str
    reminder_time: str
    color_theme: str
    days_of_week: Optional[str] = "1,2,3,4,5,6,7"


class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    habit_name: Optional[str] = None
    category: Optional[str] = None
    goal_days: Optional[int] = None
    target_per_day: Optional[int] = None
    reminder_time: Optional[str] = None
    color_theme: Optional[str] = None
    days_of_week: Optional[str] = None


class HabitResponse(HabitBase):
    id: str
    progress: int
    streak: int
    completed_today: bool

class HabitLogRequest(BaseModel):
    date: str
    status: bool

class HabitLogEntry(BaseModel):
    date: str
    status: bool

class HabitMonthResponse(BaseModel):
    habit_id: str
    logs: List[HabitLogEntry]
