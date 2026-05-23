import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.auth import UserRegister, UserLogin, UserProfile, UserProfileUpdate, Token
from config.database import get_db, User
from utils.dependencies import get_current_user
from utils.auth_utils import get_password_hash, verify_password, create_access_token
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        # Create user in MySQL
        uid = str(uuid.uuid4())
        hashed_password = get_password_hash(user.password)
        
        new_user = User(
            id=uid,
            name=user.name,
            email=user.email,
            password_hash=hashed_password,
            joined_date=datetime.now().strftime("%Y-%m-%d"),
            total_habits=0,
            current_streak=0,
            gender=user.gender
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message": "User created successfully", "user_id": uid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile", response_model=UserProfile)
async def get_profile(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == uid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    return UserProfile(
        name=user.name,
        email=user.email,
        joined_date=user.joined_date,
        total_habits=user.total_habits,
        current_streak=user.current_streak,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        daily_calorie_goal=user.daily_calorie_goal,
        step_goal=user.step_goal,
        diet_type=user.diet_type,
        allergies=user.allergies,
        daily_protein_goal=user.daily_protein_goal,
        water_goal_glasses=user.water_goal_glasses,
    )

@router.put("/profile", response_model=dict)
async def update_profile(profile_data: UserProfileUpdate, uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if profile_data.name:
        user.name = profile_data.name
    if profile_data.gender is not None:
        user.gender = profile_data.gender
    if profile_data.email:
        if profile_data.email != user.email:
            existing = db.query(User).filter(User.email == profile_data.email).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already taken")
            user.email = profile_data.email
    if profile_data.height is not None:
        user.height = profile_data.height
    if profile_data.weight is not None:
        user.weight = profile_data.weight
    if profile_data.daily_calorie_goal is not None:
        user.daily_calorie_goal = profile_data.daily_calorie_goal
    if profile_data.step_goal is not None:
        user.step_goal = profile_data.step_goal
    if profile_data.diet_type is not None:
        user.diet_type = profile_data.diet_type
    if profile_data.allergies is not None:
        user.allergies = profile_data.allergies
    if profile_data.daily_protein_goal is not None:
        user.daily_protein_goal = profile_data.daily_protein_goal
    if profile_data.water_goal_glasses is not None:
        user.water_goal_glasses = profile_data.water_goal_glasses
            
    db.commit()
    return {"message": "Profile updated successfully"}
