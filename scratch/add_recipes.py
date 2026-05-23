import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import SessionLocal, Recipe

def add():
    db = SessionLocal()
    recipes = [
        # ── Breakfast ───────────────────────────────────────
        {"food_name":"Idli","prep_time":"15 mins","cook_time":"15 mins","difficulty":"Medium","servings":4,
         "ingredients":json.dumps(["2 cups Idli rice","1 cup Urad dal","Salt to taste","Water as needed"]),
         "instructions":json.dumps(["Soak rice and dal separately for 6 hours.","Grind both to a smooth batter and mix well.","Ferment batter overnight.","Pour into greased idli moulds.","Steam for 10-12 minutes until done."]),
         "tips":json.dumps(["Fermentation is key for soft idlis.","Serve hot with sambar and coconut chutney."])},

        {"food_name":"Dosa","prep_time":"10 mins","cook_time":"5 mins","difficulty":"Medium","servings":4,
         "ingredients":json.dumps(["2 cups Idli/Dosa batter","Oil or butter for cooking","Salt to taste"]),
         "instructions":json.dumps(["Prepare fermented dosa batter.","Heat a flat non-stick pan on medium-high heat.","Pour a ladle of batter and spread in circular motion.","Drizzle oil on edges and cook until crispy.","Fold and serve with chutney and sambar."]),
         "tips":json.dumps(["Pan should be hot enough before pouring batter.","Add a pinch of fenugreek seeds to batter for crispy dosa."])},

        {"food_name":"Upma","prep_time":"5 mins","cook_time":"15 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["1 cup Semolina (Rava)","2 cups Water","1 onion chopped","Mustard seeds, Curry leaves","Green chillies","Salt and Oil"]),
         "instructions":json.dumps(["Dry roast semolina until light golden. Set aside.","Heat oil, add mustard seeds and curry leaves.","Sauté onions and chillies until translucent.","Add water and salt, bring to boil.","Slowly add roasted rava stirring continuously.","Cover and cook 3-4 mins. Serve hot."]),
         "tips":json.dumps(["Roasting rava prevents lumps.","Add lemon juice for a tangy twist."])},

        {"food_name":"Poha","prep_time":"5 mins","cook_time":"10 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["2 cups Thick Poha (flattened rice)","1 onion chopped","1 potato diced","Mustard seeds, Turmeric","Curry leaves, Green chillies","Lemon juice, Coriander"]),
         "instructions":json.dumps(["Rinse poha in water and drain. Set aside for 5 mins.","Heat oil, add mustard seeds, curry leaves and chillies.","Add onion and potato, cook until potato is soft.","Add turmeric and mix in poha gently.","Season with salt, lemon juice and coriander."]),
         "tips":json.dumps(["Don't over-soak poha or it becomes mushy.","Add roasted peanuts for extra crunch."])},

        {"food_name":"Paratha","prep_time":"15 mins","cook_time":"15 mins","difficulty":"Easy","servings":3,
         "ingredients":json.dumps(["2 cups Whole wheat flour","2 Potatoes boiled & mashed","1 tsp Cumin powder","Garam masala, Green chillies","Salt, Ghee for cooking"]),
         "instructions":json.dumps(["Mix flour with water to make a soft dough.","Combine mashed potato with spices for filling.","Roll a ball of dough, stuff with filling and seal.","Roll flat gently without breaking.","Cook on hot tawa with ghee on both sides until golden."]),
         "tips":json.dumps(["Keep filling dry to avoid breaking.","Serve with curd and pickle."])},

        {"food_name":"Oats","prep_time":"2 mins","cook_time":"5 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["1 cup Rolled oats","1.5 cups Milk or Water","1 tsp Honey","Banana slices or berries","Cinnamon powder"]),
         "instructions":json.dumps(["Bring milk or water to a boil.","Add oats and stir on medium heat.","Cook 3-5 mins until oats absorb liquid.","Add honey and cinnamon.","Top with fresh fruits and serve warm."]),
         "tips":json.dumps(["Use rolled oats for best texture.","Add chia seeds or nuts for extra nutrition."])},

        {"food_name":"Bread Toast","prep_time":"2 mins","cook_time":"5 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["2 slices Whole wheat bread","Butter or olive oil","Salt and Pepper","Optional: Eggs or avocado topping"]),
         "instructions":json.dumps(["Heat a pan or toaster.","Butter the bread slices.","Toast until golden brown on both sides.","Season with salt and pepper.","Add toppings of your choice and serve."]),
         "tips":json.dumps(["Use sourdough for more flavour.","Pair with a boiled egg for a complete breakfast."])},

        {"food_name":"Egg Omelette","prep_time":"2 mins","cook_time":"5 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["2 Eggs","1 tbsp Milk","Salt and Pepper","Chopped onion, tomato, chilli","Oil or Butter"]),
         "instructions":json.dumps(["Whisk eggs with milk, salt and pepper.","Heat butter in a pan on medium heat.","Add chopped veggies and sauté briefly.","Pour egg mixture over veggies.","Cook until set, fold and serve."]),
         "tips":json.dumps(["Low-medium heat prevents burning.","Add cheese before folding for extra richness."])},

        {"food_name":"Boiled Eggs","prep_time":"0 mins","cook_time":"10 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["2 Eggs","Water to cover","Salt for serving","Pepper (optional)"]),
         "instructions":json.dumps(["Place eggs in a pot and cover with cold water.","Bring to a boil over high heat.","Boil 6-7 mins for soft-boiled, 10 mins for hard.","Transfer to ice water to stop cooking.","Peel carefully and serve with salt."]),
         "tips":json.dumps(["Starting with cold water ensures even cooking.","Ice bath makes peeling much easier."])},

        {"food_name":"Pesarattu","prep_time":"10 mins","cook_time":"10 mins","difficulty":"Medium","servings":4,
         "ingredients":json.dumps(["2 cups Green moong dal","1 inch Ginger","2 Green chillies","Salt to taste","Oil for cooking","Chopped onion for topping"]),
         "instructions":json.dumps(["Soak moong dal for 4-6 hours.","Grind with ginger and chillies to a batter.","Add salt and mix well.","Heat tawa and pour a ladle of batter, spread thin.","Drizzle oil and cook until golden crispy.","Top with onions and serve with chutney."]),
         "tips":json.dumps(["Don't ferment the batter — use fresh.","Add cumin seeds for extra flavour."])},

        # ── Lunch ──────────────────────────────────────────
        {"food_name":"Rice","prep_time":"2 mins","cook_time":"15 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["1 cup Basmati or Long-grain rice","2 cups Water","Salt to taste","1 tsp Oil (optional)"]),
         "instructions":json.dumps(["Wash rice 2-3 times until water runs clear.","Add rice, water, salt and oil to a pot.","Bring to boil on high heat.","Reduce heat to low, cover and cook 12 mins.","Fluff with fork and serve."]),
         "tips":json.dumps(["1:2 rice to water ratio for perfect fluffy rice.","Let rice rest 5 mins after cooking before fluffing."])},

        {"food_name":"Chapati","prep_time":"15 mins","cook_time":"15 mins","difficulty":"Easy","servings":4,
         "ingredients":json.dumps(["2 cups Whole wheat flour","Water as needed","1 tsp Oil","Salt to taste"]),
         "instructions":json.dumps(["Mix flour, salt and oil.","Add water gradually to form a soft dough.","Rest dough for 10 mins.","Divide into balls and roll into thin circles.","Cook on hot tawa until brown spots appear on both sides."]),
         "tips":json.dumps(["Soft dough gives soft chapatis.","Apply ghee after cooking for extra softness."])},

        {"food_name":"Dal","prep_time":"5 mins","cook_time":"25 mins","difficulty":"Easy","servings":4,
         "ingredients":json.dumps(["1 cup Toor dal or Masoor dal","1 Tomato chopped","1 tsp Turmeric","1 tsp Cumin seeds","Salt, Oil, Coriander"]),
         "instructions":json.dumps(["Pressure cook dal with tomato, turmeric and salt.","Heat oil in a pan, add cumin seeds.","Pour over cooked dal and mix.","Simmer 5 mins and adjust consistency.","Garnish with coriander and serve."]),
         "tips":json.dumps(["Soak dal for 30 mins to speed up cooking.","A squeeze of lemon brightens the flavour."])},

        {"food_name":"Sambar","prep_time":"10 mins","cook_time":"25 mins","difficulty":"Medium","servings":4,
         "ingredients":json.dumps(["1 cup Toor dal","1 cup Mixed vegetables (Drumstick, Brinjal, Tomato)","2 tbsp Sambar powder","Tamarind water","Mustard seeds, Curry leaves, Dry red chilli"]),
         "instructions":json.dumps(["Pressure cook toor dal until soft.","Add vegetables and sambar powder to the dal.","Add tamarind water and simmer 10 mins.","Prepare tempering with mustard seeds and curry leaves.","Pour tempering over sambar and serve."]),
         "tips":json.dumps(["Drumstick gives authentic sambar flavour.","Don't skip the tempering — it makes the dish."])},

        {"food_name":"Curd Rice","prep_time":"5 mins","cook_time":"5 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["1 cup Cooked rice","1 cup Fresh curd (yogurt)","Mustard seeds, Curry leaves","1 Green chilli","Pomegranate seeds (optional)","Salt to taste"]),
         "instructions":json.dumps(["Let cooked rice cool slightly.","Mix curd and salt into the rice well.","Heat oil and add mustard seeds and curry leaves.","Pour tempering over curd rice and mix.","Garnish with pomegranate seeds and serve."]),
         "tips":json.dumps(["Use thick curd for better taste.","Serve chilled for a refreshing meal."])},

        {"food_name":"Paneer Curry","prep_time":"10 mins","cook_time":"20 mins","difficulty":"Medium","servings":3,
         "ingredients":json.dumps(["200g Paneer cubed","2 Onions","2 Tomatoes pureed","Ginger-garlic paste","Cumin, Coriander, Garam masala","Cream (optional)","Oil, Salt"]),
         "instructions":json.dumps(["Sauté onions until golden brown.","Add ginger-garlic paste and cook 2 mins.","Add tomato puree and spices. Cook 5 mins.","Add paneer cubes and stir gently.","Add water for gravy and simmer 5 mins.","Finish with cream and serve."]),
         "tips":json.dumps(["Don't overcook paneer or it becomes rubbery.","Use store-bought paneer or make fresh at home."])},

        {"food_name":"Fish Curry","prep_time":"15 mins","cook_time":"25 mins","difficulty":"Medium","servings":3,
         "ingredients":json.dumps(["400g Fish (Rohu or Pomfret)","2 Onions sliced","Tamarind extract","Coconut milk or Coconut paste","Red chilli powder, Turmeric, Coriander powder","Curry leaves, Oil, Salt"]),
         "instructions":json.dumps(["Marinate fish with turmeric and salt.","Sauté onions until golden in oil.","Add spices and coconut paste, cook 3 mins.","Add tamarind water and bring to a boil.","Add fish and cook gently 8-10 mins.","Garnish with curry leaves and serve."]),
         "tips":json.dumps(["Don't stir too much to avoid breaking the fish.","Coconut oil gives authentic coastal flavour."])},

        {"food_name":"Egg Curry","prep_time":"5 mins","cook_time":"20 mins","difficulty":"Easy","servings":3,
         "ingredients":json.dumps(["4 Hard-boiled eggs","2 Onions chopped","2 Tomatoes","Ginger-garlic paste","Chilli powder, Turmeric, Garam masala","Oil, Salt, Coriander"]),
         "instructions":json.dumps(["Slit hard-boiled eggs and lightly fry until golden.","Sauté onions until deeply caramelised.","Add ginger-garlic paste and cook well.","Add tomatoes and spices, cook until oil separates.","Add eggs and water, simmer 5 mins.","Garnish with coriander and serve."]),
         "tips":json.dumps(["Caramelising onions deeply is the secret to great curry.","Score the eggs before frying so they absorb the gravy."])},

        {"food_name":"Biryani Veg","prep_time":"20 mins","cook_time":"30 mins","difficulty":"Hard","servings":4,
         "ingredients":json.dumps(["2 cups Basmati rice","1 cup Mixed vegetables","1/2 cup Yogurt","Whole spices (Cardamom, Cloves, Cinnamon)","Fried onions, Saffron milk","Mint and Coriander leaves","Biryani masala"]),
         "instructions":json.dumps(["Cook rice 70% done with whole spices.","Cook vegetables with yogurt and biryani masala.","Layer rice and vegetables in a heavy pot.","Top with fried onions, mint, coriander and saffron milk.","Cover tightly and dum cook on low heat 20 mins.","Fluff gently and serve with Raita."]),
         "tips":json.dumps(["Use long-grain Basmati for best results.","Seal the pot with dough for authentic dum cooking."])},

        {"food_name":"Biryani Chicken","prep_time":"30 mins","cook_time":"40 mins","difficulty":"Hard","servings":4,
         "ingredients":json.dumps(["500g Chicken","2 cups Basmati rice","1 cup Yogurt","2 Onions thinly sliced","Whole spices","Saffron, Mint, Coriander","Ghee, Oil, Biryani masala"]),
         "instructions":json.dumps(["Marinate chicken with yogurt and biryani masala for 2 hours.","Fry onions until golden brown (birista).","Cook chicken until 80% done.","Cook rice 70% with whole spices.","Layer rice over chicken in a heavy pot.","Top with birista, mint, saffron and dum cook 25 mins."]),
         "tips":json.dumps(["Marinating the chicken longer makes it more tender.","A heavy cast iron pot retains heat best for dum cooking."])},

        {"food_name":"Rajma","prep_time":"10 mins","cook_time":"35 mins","difficulty":"Easy","servings":4,
         "ingredients":json.dumps(["1 cup Kidney beans (soaked overnight)","2 Onions chopped","2 Tomatoes pureed","Ginger-garlic paste","Rajma masala, Cumin, Turmeric","Salt, Oil, Coriander"]),
         "instructions":json.dumps(["Pressure cook soaked rajma until very soft.","Sauté onions until golden.","Add ginger-garlic paste and cook 2 mins.","Add tomato puree, rajma masala and cook until oil separates.","Add cooked rajma and mash a few beans.","Simmer 10 mins and garnish with coriander."]),
         "tips":json.dumps(["Soak rajma overnight for faster cooking.","Mashing some beans gives a thicker, creamier gravy."])},

        {"food_name":"Chana Masala","prep_time":"10 mins","cook_time":"30 mins","difficulty":"Medium","servings":4,
         "ingredients":json.dumps(["2 cups Chickpeas (soaked overnight)","2 Onions","2 Tomatoes","Chana masala powder","Amchur, Cumin, Coriander powder","Oil, Salt, Fresh coriander"]),
         "instructions":json.dumps(["Pressure cook soaked chickpeas until soft.","Sauté onions until dark golden brown.","Add tomatoes and all spices, cook until thick.","Add chickpeas and mix well.","Simmer 10 mins, add amchur for sourness.","Garnish with coriander and serve with bhature or rice."]),
         "tips":json.dumps(["Deeply browning onions and tomatoes gives restaurant flavour.","Amchur (dry mango powder) is the key souring agent."])},

        # ── Dinner ─────────────────────────────────────────
        {"food_name":"Roti","prep_time":"10 mins","cook_time":"15 mins","difficulty":"Easy","servings":4,
         "ingredients":json.dumps(["2 cups Whole wheat flour","Water as needed","Salt to taste"]),
         "instructions":json.dumps(["Mix flour and salt, add water to form soft dough.","Rest for 10 mins.","Divide dough into small balls.","Roll each ball into a thin circle.","Cook on hot tawa until puffed and brown spots appear."]),
         "tips":json.dumps(["Roast directly on flame for a puffed roti.","Soft dough = soft roti. Don't add too much flour."])},

        {"food_name":"Mixed Veg Curry","prep_time":"10 mins","cook_time":"20 mins","difficulty":"Easy","servings":3,
         "ingredients":json.dumps(["1 cup Mixed vegetables (Carrot, Peas, Potato, Beans)","1 Onion chopped","1 Tomato","Cumin, Turmeric, Coriander powder","Oil, Salt, Garam masala"]),
         "instructions":json.dumps(["Heat oil and sauté cumin and onions until golden.","Add tomatoes and spices. Cook 3 mins.","Add diced vegetables and stir well.","Add water, cover and cook until vegetables are tender.","Adjust seasoning and serve."]),
         "tips":json.dumps(["Cut vegetables in similar sizes for even cooking.","Add coconut milk for a South Indian variation."])},

        {"food_name":"Grilled Chicken","prep_time":"15 mins","cook_time":"20 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["200g Chicken breast","1 tbsp Olive oil","Lemon juice","Garlic powder, Paprika","Salt, Pepper, Mixed herbs"]),
         "instructions":json.dumps(["Mix oil, lemon juice and all spices for marinade.","Coat chicken and marinate 30 mins (or overnight).","Preheat grill or pan on high heat.","Grill chicken 6-7 mins each side until cooked through.","Rest 5 mins before slicing and serving."]),
         "tips":json.dumps(["Internal temp should reach 75°C for safe chicken.","Resting keeps the juices inside the chicken."])},

        {"food_name":"Mushroom Curry","prep_time":"10 mins","cook_time":"20 mins","difficulty":"Easy","servings":3,
         "ingredients":json.dumps(["250g Button mushrooms","1 Onion","2 Tomatoes","Ginger-garlic paste","Cumin, Coriander, Garam masala","Cream (optional), Oil, Salt"]),
         "instructions":json.dumps(["Sauté onions until golden.","Add ginger-garlic paste and cook 2 mins.","Add tomatoes and spices, cook until oil separates.","Add mushrooms and mix well.","Cook 8-10 mins until mushrooms are tender.","Add cream if desired and serve."]),
         "tips":json.dumps(["Don't wash mushrooms — wipe with a damp cloth.","High heat helps mushrooms cook without becoming watery."])},

        # ── Snacks ─────────────────────────────────────────
        {"food_name":"Banana","prep_time":"0 mins","cook_time":"0 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["1 ripe Banana"]),
         "instructions":json.dumps(["Peel the banana.","Eat as is or slice and add to yogurt or oats.","Can also be blended into a smoothie."]),
         "tips":json.dumps(["Ripe bananas are sweeter and easier to digest.","Freeze overripe bananas for smoothies."])},

        {"food_name":"Apple","prep_time":"2 mins","cook_time":"0 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["1 Apple","Peanut butter (optional)"]),
         "instructions":json.dumps(["Wash the apple thoroughly.","Slice and remove the core.","Eat as is or pair with peanut butter for extra protein."]),
         "tips":json.dumps(["Eat with the skin for maximum fibre.","Pair with protein like nuts to keep you full longer."])},

        {"food_name":"Peanuts","prep_time":"5 mins","cook_time":"10 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["100g Raw peanuts","Salt to taste","Oil (optional)"]),
         "instructions":json.dumps(["Heat a dry pan on medium heat.","Add peanuts and roast stirring continuously.","Roast 8-10 mins until they turn light brown and fragrant.","Add salt and toss.","Cool and store in an airtight container."]),
         "tips":json.dumps(["Dry roast for healthiest version — no oil needed.","Watch carefully — peanuts burn quickly at the end."])},

        {"food_name":"Sprouts","prep_time":"5 mins","cook_time":"5 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["1 cup Mixed sprouts (Moong, Chana)","Lemon juice","Chaat masala","Chopped tomato, onion, coriander","Salt to taste"]),
         "instructions":json.dumps(["Rinse sprouts well.","Steam for 3-4 mins if preferred cooked.","Mix with chopped vegetables.","Season with lemon, chaat masala and salt.","Toss and serve immediately."]),
         "tips":json.dumps(["Sprouts are most nutritious eaten raw or lightly steamed.","Add cucumber and pomegranate for extra freshness."])},

        {"food_name":"Roasted Chana","prep_time":"2 mins","cook_time":"0 mins","difficulty":"Easy","servings":2,
         "ingredients":json.dumps(["100g Roasted chana (dal)","Chaat masala","Lemon juice","Salt (optional)"]),
         "instructions":json.dumps(["Take roasted chana in a bowl.","Sprinkle chaat masala and salt.","Squeeze lemon juice and toss.","Serve as a crunchy healthy snack."]),
         "tips":json.dumps(["Buy pre-roasted chana from supermarkets.","Great pre-workout snack for energy."])},

        {"food_name":"Greek Yogurt","prep_time":"2 mins","cook_time":"0 mins","difficulty":"Easy","servings":1,
         "ingredients":json.dumps(["1 cup Greek yogurt","1 tsp Honey","Mixed berries or banana slices","Granola or nuts (optional)"]),
         "instructions":json.dumps(["Scoop yogurt into a bowl.","Drizzle honey on top.","Add fruits and granola.","Mix or eat in layers."]),
         "tips":json.dumps(["Greek yogurt has more protein than regular yogurt.","Choose plain, unsweetened for less sugar."])},

        {"food_name":"Protein Bar","prep_time":"10 mins","cook_time":"0 mins","difficulty":"Easy","servings":6,
         "ingredients":json.dumps(["1 cup Rolled oats","1/2 cup Peanut butter","1/4 cup Honey","1/2 cup Protein powder","2 tbsp Dark chocolate chips","1/4 cup Mixed seeds"]),
         "instructions":json.dumps(["Mix all ingredients together in a bowl.","Press firmly into a lined baking tray.","Refrigerate for 2 hours until set.","Cut into bars.","Store in fridge for up to a week."]),
         "tips":json.dumps(["Adjust honey to change sweetness.","Add dried cranberries for a fruity twist."])},
    ]

    added = 0
    for r in recipes:
        existing = db.query(Recipe).filter(Recipe.food_name == r["food_name"]).first()
        if not existing:
            db.add(Recipe(**r))
            added += 1
        else:
            # Update existing
            for k, v in r.items():
                setattr(existing, k, v)
            added += 1

    db.commit()
    db.close()
    print(f"Done! {added} recipes added/updated.")

if __name__ == "__main__":
    add()
