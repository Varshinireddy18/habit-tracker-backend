from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class GoalBase(BaseModel):
    goal_name: str
    target_value: int = Field(..., gt=0)
    actual_value: int = Field(0, ge=0)
    deadline: str
    days_of_week: Optional[str] = "1,2,3,4,5,6,7"


class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    target_value: Optional[int] = None
    actual_value: Optional[int] = None
    deadline: Optional[str] = None
    days_of_week: Optional[str] = None


class GoalResponse(GoalBase):
    id: str
    status_percentage: int
