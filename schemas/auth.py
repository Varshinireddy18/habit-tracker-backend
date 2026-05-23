from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    gender: Optional[str] = None  # 'male' or 'female'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    name: str
    email: EmailStr
    joined_date: str
    total_habits: int
    current_streak: int
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    daily_calorie_goal: Optional[int] = 2000
    step_goal: Optional[int] = 10000
    diet_type: Optional[str] = "Veg"
    allergies: Optional[str] = None
    daily_protein_goal: Optional[float] = 50.0
    water_goal_glasses: Optional[int] = 8

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    daily_calorie_goal: Optional[int] = None
    step_goal: Optional[int] = None
    diet_type: Optional[str] = None
    allergies: Optional[str] = None
    daily_protein_goal: Optional[float] = None
    water_goal_glasses: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
