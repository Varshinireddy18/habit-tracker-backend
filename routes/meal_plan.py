
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from config.database import get_db, MealPlan
from utils.dependencies import get_current_user
from config.gemini import model
import json

router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Planning"]
)

@router.get("/generate")
async def generate_meal_plan(
    diet: str = Query(..., pattern="^(Veg|Non-Veg|Vegan)$"),
    goal: str = Query(..., pattern="^(Weight Loss|Maintain Weight|Weight Gain)$"),
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:

        prompt = f"""
        Create a professional 7-day meal plan.

        Diet Type: {diet}

        Goal: {goal}

        Return ONLY valid JSON.

        Format:

        {{
          "week_start_date": "2026-06-01",
          "days": [
            {{
              "day": "Monday",
              "meals": [
                {{
                  "meal_type": "Breakfast",
                  "food_name": "Oats",
                  "calories": 300,
                  "emoji": "🥣"
                }},
                {{
                  "meal_type": "Lunch",
                  "food_name": "Rice",
                  "calories": 500,
                  "emoji": "🍛"
                }},
                {{
                  "meal_type": "Dinner",
                  "food_name": "Paneer Curry",
                  "calories": 450,
                  "emoji": "🧀"
                }},
                {{
                  "meal_type": "Snack",
                  "food_name": "Apple",
                  "calories": 100,
                  "emoji": "🍎"
                }}
              ],
              "total_calories": 1350
            }}
          ]
        }}

        Generate all 7 days.
        """

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "")

        meal_plan = json.loads(text)

        return meal_plan

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini Error: {str(e)}"
        )


@router.get("/current")
async def get_current_meal_plan(
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=404,
        detail="No saved meal plan. Generate a new plan."
    )


