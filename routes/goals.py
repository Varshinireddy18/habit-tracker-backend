from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.goals import GoalCreate, GoalUpdate, GoalResponse
from config.database import get_db, Goal
from utils.dependencies import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/goals", tags=["Goals"])

@router.post("", response_model=dict)
async def create_goal(goal: GoalCreate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        goal_id = str(uuid.uuid4())
        goal_data = goal.dict()
        
        # Calculate percentage
        status_percentage = int(round((goal.actual_value / goal.target_value) * 100)) if goal.target_value > 0 else 0
        
        new_goal = Goal(
            id=goal_id,
            user_id=uid,
            **goal_data,
            status_percentage=status_percentage,
            created_at=datetime.now().isoformat()
        )
        
        db.add(new_goal)
        db.commit()
        
        return {"message": "Goal created successfully", "goal_id": goal_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[GoalResponse])
async def get_goals(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        goals = db.query(Goal).filter(Goal.user_id == uid).all()
        return [GoalResponse(
            id=goal.id,
            goal_name=goal.goal_name,
            target_value=goal.target_value,
            actual_value=goal.actual_value,
            deadline=goal.deadline,
            status_percentage=goal.status_percentage,
            days_of_week=goal.days_of_week
        ) for goal in goals]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{goal_id}", response_model=dict)
async def update_goal(goal_id: str, goal: GoalUpdate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == uid).first()
    
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    update_data = {k: v for k, v in goal.dict().items() if v is not None}
    for key, value in update_data.items():
        setattr(db_goal, key, value)
    
    # Recalculate percentage
    actual = db_goal.actual_value
    target = db_goal.target_value
    db_goal.status_percentage = int(round((actual / target) * 100)) if target > 0 else 0
    
    db.commit()
    
    return {"message": "Goal updated successfully", "status_percentage": db_goal.status_percentage}

@router.delete("/{goal_id}", response_model=dict)
async def delete_goal(goal_id: str, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == uid).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    db.delete(db_goal)
    db.commit()
    return {"message": "Goal deleted successfully"}
