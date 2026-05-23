from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db, Recipe
from schemas.food import RecipeResponse
import json

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/{food_name}", response_model=RecipeResponse)
async def get_recipe(
    food_name: str,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.food_name == food_name).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    return RecipeResponse(
        food_name=recipe.food_name,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        difficulty=recipe.difficulty,
        servings=recipe.servings,
        ingredients=json.loads(recipe.ingredients),
        instructions=json.loads(recipe.instructions),
        tips=json.loads(recipe.tips)
    )
