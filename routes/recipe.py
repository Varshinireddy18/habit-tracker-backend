from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db, Recipe
from schemas.food import RecipeResponse
from config.gemini import client
from google.genai import types
import json, traceback

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/{food_name}", response_model=RecipeResponse)
def get_recipe(
    food_name: str,
    calories: Optional[int] = None,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.food_name == food_name).first()
    
    # If no calories specified and it exists in the database, return the static version
    if recipe and not calories:
        return RecipeResponse(
            food_name=str(recipe.food_name),
            prep_time=str(recipe.prep_time),
            cook_time=str(recipe.cook_time),
            difficulty=str(recipe.difficulty),
            servings=int(str(recipe.servings)),
            ingredients=json.loads(str(recipe.ingredients)),
            instructions=json.loads(str(recipe.instructions)),
            tips=json.loads(str(recipe.tips))
        )
        
    # Otherwise, generate a custom recipe via Gemini
    try:
        cal_str = f" exactly {calories} calories total." if calories else "."
        prompt = f"""You are a professional chef and nutritionist.
Generate a recipe for '{food_name}'.
The recipe MUST be portioned to contain{cal_str} Include exact measurements (e.g. grams, ml) for each ingredient to match this calorie target.

Respond ONLY with a valid JSON object in this exact format (no markdown, no explanation):
{{
  "food_name": "{food_name}",
  "prep_time": "15 mins",
  "cook_time": "20 mins",
  "difficulty": "Easy",
  "servings": 1,
  "ingredients": ["100g chicken breast", "1 tbsp olive oil"],
  "instructions": ["Chop chicken", "Fry in oil"],
  "tips": ["Serve hot"]
}}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Content(parts=[types.Part(text=prompt)])]
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
        
        return RecipeResponse(
            food_name=result.get("food_name", food_name),
            prep_time=result.get("prep_time", "10 mins"),
            cook_time=result.get("cook_time", "20 mins"),
            difficulty=result.get("difficulty", "Medium"),
            servings=result.get("servings", 1),
            ingredients=result.get("ingredients", []),
            instructions=result.get("instructions", []),
            tips=result.get("tips", [])
        )
    except Exception as e:
        err_msg = f"{type(e).__name__}: {e}"
        print(f"Recipe generation failed: {err_msg}")
        traceback.print_exc()
        # Fallback to database if available
        if recipe:
            return RecipeResponse(
                food_name=str(recipe.food_name),
                prep_time=str(recipe.prep_time),
                cook_time=str(recipe.cook_time),
                difficulty=str(recipe.difficulty),
                servings=int(str(recipe.servings)),
                ingredients=json.loads(str(recipe.ingredients)),
                instructions=json.loads(str(recipe.instructions)),
                tips=json.loads(str(recipe.tips))
            )
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {err_msg}")
