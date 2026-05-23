import json
from sqlalchemy.orm import Session
from config.database import SessionLocal, Food, Recipe

def populate():
    db: Session = SessionLocal()
    
    # ── Food Data ─────────────────────────────────────────
    foods = [
        # BREAKFAST
        {"name": "Idli", "emoji": "⚪", "calories": 70, "protein": 2.0, "carbs": 15.0, "fat": 0.5, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 piece"},
        {"name": "Dosa", "emoji": "🥞", "calories": 120, "protein": 3.0, "carbs": 25.0, "fat": 1.5, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 piece"},
        {"name": "Upma", "emoji": "🥣", "calories": 180, "protein": 4.5, "carbs": 30.0, "fat": 4.0, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 cup"},
        {"name": "Poha", "emoji": "🍚", "calories": 160, "protein": 3.5, "carbs": 28.0, "fat": 3.5, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 cup"},
        {"name": "Paratha", "emoji": "🫓", "calories": 200, "protein": 5.0, "carbs": 35.0, "fat": 6.0, "diet_type": "Veg", "meal_type": "Breakfast", "serving_size": "1 piece"},
        {"name": "Oats", "emoji": "🥣", "calories": 150, "protein": 6.0, "carbs": 25.0, "fat": 3.0, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 cup"},
        {"name": "Bread Toast", "emoji": "🍞", "calories": 160, "protein": 6.0, "carbs": 30.0, "fat": 2.0, "diet_type": "Veg", "meal_type": "Breakfast", "serving_size": "2 slices"},
        {"name": "Egg Omelette", "emoji": "🍳", "calories": 180, "protein": 14.0, "carbs": 2.0, "fat": 12.0, "diet_type": "Non-Veg", "meal_type": "Breakfast", "serving_size": "2 eggs"},
        {"name": "Boiled Eggs", "emoji": "🥚", "calories": 140, "protein": 12.0, "carbs": 1.0, "fat": 10.0, "diet_type": "Non-Veg", "meal_type": "Breakfast", "serving_size": "2 eggs"},
        {"name": "Pesarattu", "emoji": "🥞", "calories": 140, "protein": 7.0, "carbs": 24.0, "fat": 2.0, "diet_type": "Vegan", "meal_type": "Breakfast", "serving_size": "1 piece"},
        
        # LUNCH
        {"name": "Rice", "emoji": "🍚", "calories": 200, "protein": 4.0, "carbs": 45.0, "fat": 0.5, "diet_type": "Vegan", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Chapati", "emoji": "🫓", "calories": 80, "protein": 3.0, "carbs": 15.0, "fat": 1.0, "diet_type": "Veg", "meal_type": "Lunch", "serving_size": "1 piece"},
        {"name": "Dal", "emoji": "🥣", "calories": 150, "protein": 9.0, "carbs": 24.0, "fat": 2.5, "diet_type": "Vegan", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Sambar", "emoji": "🥣", "calories": 80, "protein": 3.0, "carbs": 14.0, "fat": 2.0, "diet_type": "Vegan", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Curd Rice", "emoji": "🍚", "calories": 200, "protein": 6.0, "carbs": 35.0, "fat": 4.0, "diet_type": "Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Paneer Curry", "emoji": "🥘", "calories": 280, "protein": 12.0, "carbs": 10.0, "fat": 22.0, "diet_type": "Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Chicken Curry", "emoji": "🍗", "calories": 250, "protein": 25.0, "carbs": 8.0, "fat": 14.0, "diet_type": "Non-Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Fish Curry", "emoji": "🐟", "calories": 200, "protein": 22.0, "carbs": 6.0, "fat": 10.0, "diet_type": "Non-Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Egg Curry", "emoji": "🥚", "calories": 220, "protein": 14.0, "carbs": 8.0, "fat": 15.0, "diet_type": "Non-Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Biryani Veg", "emoji": "🍲", "calories": 300, "protein": 8.0, "carbs": 55.0, "fat": 6.0, "diet_type": "Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Biryani Chicken", "emoji": "🍲", "calories": 400, "protein": 28.0, "carbs": 50.0, "fat": 10.0, "diet_type": "Non-Veg", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Rajma", "emoji": "🥣", "calories": 230, "protein": 14.0, "carbs": 40.0, "fat": 2.0, "diet_type": "Vegan", "meal_type": "Lunch", "serving_size": "1 cup"},
        {"name": "Chana Masala", "emoji": "🥣", "calories": 210, "protein": 10.0, "carbs": 35.0, "fat": 4.0, "diet_type": "Vegan", "meal_type": "Lunch", "serving_size": "1 cup"},
        
        # DINNER
        {"name": "Roti", "emoji": "🫓", "calories": 80, "protein": 3.0, "carbs": 15.0, "fat": 1.0, "diet_type": "Veg", "meal_type": "Dinner", "serving_size": "1 piece"},
        {"name": "Mixed Veg Curry", "emoji": "🥗", "calories": 150, "protein": 5.0, "carbs": 20.0, "fat": 6.0, "diet_type": "Vegan", "meal_type": "Dinner", "serving_size": "1 cup"},
        {"name": "Palak Paneer", "emoji": "🥘", "calories": 240, "protein": 14.0, "carbs": 12.0, "fat": 18.0, "diet_type": "Veg", "meal_type": "Dinner", "serving_size": "1 cup"},
        {"name": "Grilled Chicken", "emoji": "🍗", "calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6, "diet_type": "Non-Veg", "meal_type": "Dinner", "serving_size": "100g"},
        {"name": "Dal Tadka", "emoji": "🥣", "calories": 170, "protein": 10.0, "carbs": 26.0, "fat": 4.0, "diet_type": "Vegan", "meal_type": "Dinner", "serving_size": "1 cup"},
        {"name": "Tofu Stir Fry", "emoji": "🥘", "calories": 150, "protein": 12.0, "carbs": 10.0, "fat": 8.0, "diet_type": "Vegan", "meal_type": "Dinner", "serving_size": "1 cup"},
        {"name": "Mushroom Curry", "emoji": "🍄", "calories": 130, "protein": 6.0, "carbs": 12.0, "fat": 7.0, "diet_type": "Vegan", "meal_type": "Dinner", "serving_size": "1 cup"},
        
        # SNACKS
        {"name": "Banana", "emoji": "🍌", "calories": 90, "protein": 1.1, "carbs": 23.0, "fat": 0.3, "diet_type": "Vegan", "meal_type": "Snack", "serving_size": "1 piece"},
        {"name": "Apple", "emoji": "🍎", "calories": 80, "protein": 0.5, "carbs": 20.0, "fat": 0.3, "diet_type": "Vegan", "meal_type": "Snack", "serving_size": "1 piece"},
        {"name": "Peanuts", "emoji": "🥜", "calories": 170, "protein": 7.5, "carbs": 6.0, "fat": 14.0, "diet_type": "Vegan", "meal_type": "Snack", "serving_size": "30g"},
        {"name": "Sprouts", "emoji": "🥗", "calories": 100, "protein": 8.0, "carbs": 18.0, "fat": 0.5, "diet_type": "Vegan", "meal_type": "Snack", "serving_size": "1 cup"},
        {"name": "Roasted Chana", "emoji": "🥜", "calories": 120, "protein": 6.0, "carbs": 20.0, "fat": 2.0, "diet_type": "Vegan", "meal_type": "Snack", "serving_size": "30g"},
        {"name": "Greek Yogurt", "emoji": "🥣", "calories": 130, "protein": 12.0, "carbs": 6.0, "fat": 5.0, "diet_type": "Veg", "meal_type": "Snack", "serving_size": "1 cup"},
        {"name": "Protein Bar", "emoji": "🍫", "calories": 200, "protein": 20.0, "carbs": 15.0, "fat": 8.0, "diet_type": "Veg", "meal_type": "Snack", "serving_size": "1 bar"},
    ]
    
    for f in foods:
        existing = db.query(Food).filter(Food.name == f["name"]).first()
        if not existing:
            db.add(Food(**f))
    
    # ── Recipe Data ───────────────────────────────────────
    recipes = [
        {
            "food_name": "Dal Tadka",
            "prep_time": "10 mins",
            "cook_time": "20 mins",
            "difficulty": "Easy",
            "servings": 4,
            "ingredients": json.dumps([
                "1 cup Yellow Moong Dal",
                "1 onion, finely chopped",
                "2 tomatoes, chopped",
                "1 tsp Cumin seeds",
                "2 Dry red chillies",
                "1 tbsp Ghee or Oil",
                "Turmeric, Salt, Red chilli powder",
                "Fresh coriander for garnish"
            ]),
            "instructions": json.dumps([
                "Wash and pressure cook dal with turmeric and salt until soft.",
                "Heat ghee in a pan, add cumin seeds and dry red chillies.",
                "Add onions and sauté until golden brown.",
                "Add tomatoes and cook until soft.",
                "Pour the tempering over the cooked dal.",
                "Garnish with fresh coriander and serve hot."
            ]),
            "tips": json.dumps([
                "Add a pinch of Hing for better digestion.",
                "Use butter for a richer flavor."
            ])
        },
        {
            "food_name": "Palak Paneer",
            "prep_time": "15 mins",
            "cook_time": "20 mins",
            "difficulty": "Medium",
            "servings": 3,
            "ingredients": json.dumps([
                "200g Paneer cubes",
                "1 bunch Spinach (Palak)",
                "1 onion, chopped",
                "1 tbsp Ginger-Garlic paste",
                "2 Green chillies",
                "1/2 cup Fresh cream",
                "Garam masala, Kasuri methi"
            ]),
            "instructions": json.dumps([
                "Blanch spinach in hot water and then immediately in cold water.",
                "Grind blanched spinach with green chillies into a smooth paste.",
                "Sauté onions and ginger-garlic paste until brown.",
                "Add spinach puree and spices, cook for 5 minutes.",
                "Add paneer cubes and fresh cream.",
                "Simmer for 2 minutes and serve with Roti."
            ]),
            "tips": json.dumps([
                "Lightly fry paneer cubes before adding for better texture.",
                "Don't overcook spinach to maintain green color."
            ])
        },
        {
            "food_name": "Chicken Curry",
            "prep_time": "15 mins",
            "cook_time": "35 mins",
            "difficulty": "Medium",
            "servings": 4,
            "ingredients": json.dumps([
                "500g Chicken, cut into pieces",
                "2 large onions, sliced",
                "2 tomatoes, pureed",
                "1 tbsp Ginger-Garlic paste",
                "Curry powder, Turmeric, Cumin",
                "2 tbsp Oil",
                "Fresh coriander"
            ]),
            "instructions": json.dumps([
                "Heat oil and sauté onions until deep golden brown.",
                "Add ginger-garlic paste and chicken pieces. Sear well.",
                "Add tomato puree and all spices.",
                "Cover and cook on low heat until chicken is tender.",
                "Add water to adjust consistency.",
                "Garnish with coriander and serve with Rice."
            ]),
            "tips": json.dumps([
                "Marinate chicken with yogurt for 30 mins for softness.",
                "Slow cooking enhances the flavor."
            ])
        },
        {
            "food_name": "Tofu Stir Fry",
            "prep_time": "10 mins",
            "cook_time": "15 mins",
            "difficulty": "Easy",
            "servings": 2,
            "ingredients": json.dumps([
                "200g Firm Tofu, cubed",
                "1 cup Bell peppers, sliced",
                "1/2 cup Broccoli florets",
                "2 tbsp Soy sauce",
                "1 tbsp Sesame oil",
                "1 tsp Ginger, grated",
                "Sesame seeds for garnish"
            ]),
            "instructions": json.dumps([
                "Press tofu to remove excess water and cut into cubes.",
                "Heat sesame oil and fry tofu until golden on edges.",
                "Add vegetables and stir-fry on high heat for 3-4 minutes.",
                "Mix in soy sauce and ginger.",
                "Cook for another 2 minutes.",
                "Garnish with sesame seeds and serve."
            ]),
            "tips": json.dumps([
                "Use high heat for crispy vegetables.",
                "Add honey or maple syrup for a sweet-salty balance."
            ])
        },
        {
            "food_name": "Vegetable Biryani",
            "prep_time": "20 mins",
            "cook_time": "30 mins",
            "difficulty": "Hard",
            "servings": 4,
            "ingredients": json.dumps([
                "2 cups Basmati Rice",
                "1 cup Mixed vegetables (Carrots, Peas, Beans)",
                "1/2 cup Yogurt",
                "Whole spices (Cardamom, Cloves, Cinnamon)",
                "Fried onions (Birista)",
                "Saffron milk",
                "Mint and Coriander leaves"
            ]),
            "instructions": json.dumps([
                "Cook rice until 70% done with whole spices.",
                "Cook vegetables with yogurt and biryani masala.",
                "Layer rice and vegetables in a heavy bottom pot.",
                "Top with fried onions, mint, coriander, and saffron milk.",
                "Cover tightly and cook on very low heat (Dum) for 15-20 mins.",
                "Fluff gently and serve with Raita."
            ]),
            "tips": json.dumps([
                "Use long-grain Basmati rice for best results.",
                "Seal the pot with dough for perfect Dum."
            ])
        }
    ]
    
    for r in recipes:
        existing = db.query(Recipe).filter(Recipe.food_name == r["food_name"]).first()
        if not existing:
            db.add(Recipe(**r))
            
    db.commit()
    db.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    populate()
