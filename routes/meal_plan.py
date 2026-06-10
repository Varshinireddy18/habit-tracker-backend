from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from google.genai import types
from config.database import get_db, User
from utils.dependencies import get_current_user
from config.gemini import client
import json
import os
import random
from datetime import datetime

router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Planning"]
)

# ── Diet-aware meal libraries for mock fallback ─────────────────────────────

MEAL_LIBRARY = {
    "Vegan": {
        "Breakfast": [
            {"food_name": "Oat Porridge with Berries", "calories": 280, "emoji": "🫐"},
            {"food_name": "Smoothie Bowl with Banana & Chia", "calories": 320, "emoji": "🍌"},
            {"food_name": "Avocado Toast on Multigrain", "calories": 300, "emoji": "🥑"},
            {"food_name": "Tofu Scramble with Veggies", "calories": 260, "emoji": "🥦"},
            {"food_name": "Peanut Butter & Banana Wrap", "calories": 340, "emoji": "🥜"},
            {"food_name": "Coconut Yogurt with Granola", "calories": 290, "emoji": "🥥"},
            {"food_name": "Mango Overnight Oats", "calories": 310, "emoji": "🥭"},
        ],
        "Lunch": [
            {"food_name": "Lentil & Spinach Soup", "calories": 380, "emoji": "🍲"},
            {"food_name": "Chickpea Salad Wrap", "calories": 420, "emoji": "🌯"},
            {"food_name": "Black Bean Tacos", "calories": 460, "emoji": "🌮"},
            {"food_name": "Quinoa Buddha Bowl", "calories": 490, "emoji": "🥗"},
            {"food_name": "Mushroom Fried Rice", "calories": 440, "emoji": "🍄"},
            {"food_name": "Pea & Mint Risotto", "calories": 410, "emoji": "🌿"},
            {"food_name": "Tofu Stir Fry with Brown Rice", "calories": 470, "emoji": "🥡"},
        ],
        "Dinner": [
            {"food_name": "Baked Sweet Potato & Lentils", "calories": 400, "emoji": "🍠"},
            {"food_name": "Vegan Thai Green Curry", "calories": 450, "emoji": "🥬"},
            {"food_name": "Stuffed Bell Peppers (Quinoa)", "calories": 380, "emoji": "🫑"},
            {"food_name": "Chickpea & Tomato Stew", "calories": 360, "emoji": "🍅"},
            {"food_name": "Zucchini Pasta with Pesto", "calories": 390, "emoji": "🍝"},
            {"food_name": "Lentil Dahl with Roti", "calories": 430, "emoji": "🫓"},
            {"food_name": "Vegetable Biryani", "calories": 480, "emoji": "🍛"},
        ],
    },
    "Veg": {
        "Breakfast": [
            {"food_name": "Masala Oats with Milk", "calories": 310, "emoji": "🥣"},
            {"food_name": "Paneer Paratha with Curd", "calories": 380, "emoji": "🧀"},
            {"food_name": "Greek Yogurt with Honey & Walnuts", "calories": 290, "emoji": "🍯"},
            {"food_name": "Vegetable Poha", "calories": 270, "emoji": "🌾"},
            {"food_name": "Idli with Sambar", "calories": 250, "emoji": "🍚"},
            {"food_name": "Besan Cheela with Chutney", "calories": 300, "emoji": "🥞"},
            {"food_name": "Ragi Porridge with Banana", "calories": 280, "emoji": "🍌"},
        ],
        "Lunch": [
            {"food_name": "Dal Tadka & Steamed Rice", "calories": 520, "emoji": "🍛"},
            {"food_name": "Paneer Butter Masala & Roti", "calories": 580, "emoji": "🧀"},
            {"food_name": "Rajma Chawal", "calories": 550, "emoji": "🫘"},
            {"food_name": "Chole Bhature", "calories": 620, "emoji": "🍞"},
            {"food_name": "Mixed Veg Curry & Brown Rice", "calories": 480, "emoji": "🥘"},
            {"food_name": "Palak Paneer & Tandoori Roti", "calories": 500, "emoji": "🥬"},
            {"food_name": "Aloo Gobi Sabzi & Roti", "calories": 460, "emoji": "🥔"},
        ],
        "Dinner": [
            {"food_name": "Paneer Tikka & Salad", "calories": 420, "emoji": "🧀"},
            {"food_name": "Moong Dal Khichdi", "calories": 380, "emoji": "🍲"},
            {"food_name": "Methi Thepla & Curd", "calories": 350, "emoji": "🌿"},
            {"food_name": "Vegetable Soup & Garlic Bread", "calories": 330, "emoji": "🥣"},
            {"food_name": "Egg Bhurji & Whole Wheat Roti", "calories": 400, "emoji": "🥚"},
            {"food_name": "Dosa & Coconut Chutney", "calories": 360, "emoji": "🥞"},
            {"food_name": "Tofu Palak Curry & Rice", "calories": 410, "emoji": "🥬"},
        ],
    },
    "Non-Veg": {
        "Breakfast": [
            {"food_name": "Scrambled Eggs & Whole Wheat Toast", "calories": 320, "emoji": "🍳"},
            {"food_name": "Chicken Omelette", "calories": 350, "emoji": "🥚"},
            {"food_name": "Boiled Eggs & Avocado", "calories": 300, "emoji": "🥑"},
            {"food_name": "Smoked Salmon & Greek Yogurt Bowl", "calories": 340, "emoji": "🐟"},
            {"food_name": "Egg & Cheese Sandwich", "calories": 370, "emoji": "🥪"},
            {"food_name": "Chicken Upma", "calories": 310, "emoji": "🍳"},
            {"food_name": "Tuna Salad Toast", "calories": 280, "emoji": "🐟"},
        ],
        "Lunch": [
            {"food_name": "Chicken Biryani", "calories": 620, "emoji": "🍗"},
            {"food_name": "Grilled Fish & Brown Rice", "calories": 540, "emoji": "🐟"},
            {"food_name": "Mutton Curry & Roti", "calories": 680, "emoji": "🥩"},
            {"food_name": "Prawn Masala & Rice", "calories": 580, "emoji": "🦐"},
            {"food_name": "Chicken Stir Fry & Noodles", "calories": 560, "emoji": "🍜"},
            {"food_name": "Egg Curry & Steamed Rice", "calories": 500, "emoji": "🥚"},
            {"food_name": "Tandoori Chicken & Dal", "calories": 590, "emoji": "🍗"},
        ],
        "Dinner": [
            {"food_name": "Grilled Chicken Breast & Veggies", "calories": 420, "emoji": "🍗"},
            {"food_name": "Baked Salmon with Asparagus", "calories": 450, "emoji": "🐟"},
            {"food_name": "Chicken Soup & Garlic Bread", "calories": 380, "emoji": "🍲"},
            {"food_name": "Keema Matar & Paratha", "calories": 510, "emoji": "🥩"},
            {"food_name": "Fish Tacos with Salsa", "calories": 430, "emoji": "🌮"},
            {"food_name": "Egg Fried Rice", "calories": 470, "emoji": "🍳"},
            {"food_name": "Chicken Caesar Salad", "calories": 390, "emoji": "🥗"},
        ],
    },
    "Other": {
        "Breakfast": [
            {"food_name": "Overnight Oats with Fruits", "calories": 310, "emoji": "🥣"},
            {"food_name": "Whole Grain Toast & Peanut Butter", "calories": 330, "emoji": "🍞"},
            {"food_name": "Mixed Berry Smoothie", "calories": 260, "emoji": "🫐"},
            {"food_name": "Granola & Milk Bowl", "calories": 350, "emoji": "🥛"},
            {"food_name": "Banana Pancakes", "calories": 300, "emoji": "🥞"},
            {"food_name": "Chia Seed Pudding", "calories": 280, "emoji": "🌱"},
            {"food_name": "Fruit Salad with Nuts", "calories": 240, "emoji": "🍎"},
        ],
        "Lunch": [
            {"food_name": "Lentil Soup & Sourdough", "calories": 450, "emoji": "🍲"},
            {"food_name": "Mediterranean Salad Bowl", "calories": 420, "emoji": "🥗"},
            {"food_name": "Veggie Burger & Sweet Potato Fries", "calories": 520, "emoji": "🍔"},
            {"food_name": "Hummus Wrap with Veggies", "calories": 440, "emoji": "🌯"},
            {"food_name": "Tomato Basil Pasta", "calories": 490, "emoji": "🍝"},
            {"food_name": "Minestrone Soup & Bread", "calories": 400, "emoji": "🍵"},
            {"food_name": "Grain Bowl with Roasted Veggies", "calories": 470, "emoji": "🥙"},
        ],
        "Dinner": [
            {"food_name": "Stuffed Peppers & Quinoa", "calories": 400, "emoji": "🫑"},
            {"food_name": "Mushroom Risotto", "calories": 430, "emoji": "🍄"},
            {"food_name": "Roasted Veggie & Feta Salad", "calories": 360, "emoji": "🥗"},
            {"food_name": "Sweet Potato Curry", "calories": 390, "emoji": "🍠"},
            {"food_name": "Bean Enchiladas", "calories": 450, "emoji": "🌯"},
            {"food_name": "Vegetable Noodle Soup", "calories": 340, "emoji": "🍜"},
            {"food_name": "Cauliflower Fried Rice", "calories": 380, "emoji": "🥦"},
        ],
    },
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _build_mock_plan(diet: str, goal: str) -> dict:
    """Build a full 7-day mock meal plan based on diet type."""

    # Normalize diet key
    diet_key = diet if diet in MEAL_LIBRARY else "Other"
    library = MEAL_LIBRARY[diet_key]

    # Shuffle meals so every day is different
    breakfasts = random.sample(library["Breakfast"], len(library["Breakfast"]))
    lunches = random.sample(library["Lunch"], len(library["Lunch"]))
    dinners = random.sample(library["Dinner"], len(library["Dinner"]))

    # Adjust calorie targets based on goal
    calorie_scale = 1.0
    if goal.lower() in ("weight loss", "lose weight"):
        calorie_scale = 0.85
    elif goal.lower() in ("muscle gain", "build muscle", "bulking"):
        calorie_scale = 1.20

    week_start = datetime.now().strftime("%Y-%m-%d")
    days_data = []

    for i, day in enumerate(DAYS):
        b = breakfasts[i % len(breakfasts)]
        l = lunches[i % len(lunches)]
        d = dinners[i % len(dinners)]

        b_cal = int(int(b["calories"]) * calorie_scale)
        l_cal = int(int(l["calories"]) * calorie_scale)
        d_cal = int(int(d["calories"]) * calorie_scale)

        days_data.append({
            "day": day,
            "meals": [
                {"meal_type": "Breakfast", "food_name": b["food_name"], "calories": b_cal, "emoji": b["emoji"]},
                {"meal_type": "Lunch",     "food_name": l["food_name"], "calories": l_cal, "emoji": l["emoji"]},
                {"meal_type": "Dinner",    "food_name": d["food_name"], "calories": d_cal, "emoji": d["emoji"]},
            ],
            "total_calories": b_cal + l_cal + d_cal,
        })

    return {"week_start_date": week_start, "days": days_data}


def _build_ai_prompt(diet: str, goal: str, user: User | None) -> str:
    calorie_info = f" with a daily target of {user.daily_calorie_goal} kcal" if (user and user.daily_calorie_goal) else ""
    allergies = f" Avoid: {user.allergies}." if (user and user.allergies) else ""
    return f"""You are an expert nutritionist. Generate a healthy 7-day weekly meal plan.

Diet type: {diet}
Goal: {goal}{calorie_info}{allergies}

Rules:
- Each day MUST have exactly 3 meals: Breakfast, Lunch, Dinner
- Every meal across all 7 days must be DIFFERENT (no repetitions)
- All food must strictly match the diet type ({diet})
- If diet is Vegan, absolutely NO animal products including dairy/eggs
- If diet is Veg, no meat/fish but dairy/eggs are fine
- If diet is Non-Veg, include a good mix of chicken, fish, eggs, and meat
- Adjust portion sizes to match the goal ({goal})
- Use Indian and international dishes for variety

Respond ONLY with a valid JSON object in this EXACT format (no markdown, no explanation):
{{
  "week_start_date": "YYYY-MM-DD",
  "days": [
    {{
      "day": "Monday",
      "meals": [
        {{"meal_type": "Breakfast", "food_name": "...", "calories": 300, "emoji": "🥣"}},
        {{"meal_type": "Lunch", "food_name": "...", "calories": 500, "emoji": "🍛"}},
        {{"meal_type": "Dinner", "food_name": "...", "calories": 450, "emoji": "🥘"}}
      ],
      "total_calories": 1250
    }}
  ]
}}

Generate all 7 days: Monday through Sunday."""


# ── Routes ──────────────────────────────────────────────────────────────────

@router.get("/generate")
async def generate_meal_plan(
    diet: str = Query(...),
    goal: str = Query(...),
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == uid).first()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_ACTUAL_API_KEY":
        # No valid API key → use rich diet-aware mock
        return _build_mock_plan(diet, goal)

    try:
        # pyrefly: ignore [missing-import]
        from google.genai import types
        prompt = _build_ai_prompt(diet, goal, user)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text
        if raw_text is None:
            raise ValueError("Empty response from Gemini API")
        raw = raw_text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result

    except Exception as e:
        print(f"AI meal plan failed, using mock: {e}")
        return _build_mock_plan(diet, goal)


@router.get("/current")
async def get_current_meal_plan(
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=404,
        detail="No saved meal plan"
    )
