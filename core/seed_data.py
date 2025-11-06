# core/seed_data.py
from core.models import Category, Ingredient, Recipe
from django.utils.text import slugify

# Utility function to generate unique slug
def generate_unique_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(pk=instance.pk)
    if qs.exists():
        new_slug = f"{slug}-{qs.count() + 1}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

def run():
    print("🌱 Starting manual seed data...")

    # --- Categories ---
    category_names = ["Vegetables", "Fruits", "Dairy", "Grains", "Spices", "Meat", "Seafood", "Nuts & Seeds", "Oils"]
    categories = {}
    for name in category_names:
        cat, _ = Category.objects.get_or_create(name=name)
        categories[name] = cat
    print(f"✅ Created {len(categories)} categories")

    # --- Ingredients ---
    ingredients_list = [
        ("Onion", "Vegetables"), ("Garlic", "Vegetables"), ("Carrot", "Vegetables"),
        ("Capsicum", "Vegetables"), ("Cabbage", "Vegetables"), ("Spinach", "Vegetables"),
        ("Peas", "Vegetables"), ("Cucumber", "Vegetables"),
        ("Tomato", "Fruits"), ("Apple", "Fruits"), ("Banana", "Fruits"), ("Mango", "Fruits"),
        ("Lemon", "Fruits"), ("Strawberry", "Fruits"),
        ("Milk", "Dairy"), ("Butter", "Dairy"), ("Cream", "Dairy"), ("Paneer", "Dairy"),
        ("Ghee", "Dairy"), ("Egg", "Dairy"), ("Yogurt", "Dairy"), ("Cheese", "Dairy"),
        ("Rice", "Grains"), ("Flour", "Grains"), ("Bread", "Grains"), ("Water", "Grains"),
        ("Salt", "Spices"), ("Black Pepper", "Spices"), ("Cumin", "Spices"), ("Turmeric", "Spices"),
        ("Red Chili Powder", "Spices"), ("Cardamom", "Spices"), ("Ginger", "Spices"), ("Soy Sauce", "Spices"),
        ("Chicken", "Meat"), ("Beef", "Meat"), ("Mutton", "Meat"),
        ("Fish", "Seafood"), ("Prawn", "Seafood"),
        ("Almonds", "Nuts & Seeds"), ("Cashews", "Nuts & Seeds"),
        ("Oil", "Oils")
    ]

    ingredients = {}
    for name, cat_name in ingredients_list:
        ing, _ = Ingredient.objects.get_or_create(name=name, category=categories.get(cat_name))
        ingredients[name] = ing

    print(f"✅ Created {len(ingredients)} ingredients")

    # --- Recipes ---
    recipe_data = [
    {
        "title": "Tomato Fried Rice",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Tomato", "Rice", "Onion", "Garlic", "Salt", "Butter"],
        "steps": [
            "Heat butter in a pan.",
            "Add chopped onions and garlic, sauté till golden.",
            "Add chopped tomatoes and cook until soft.",
            "Add boiled rice, salt, and mix well.",
            "Serve hot."
        ]
    },
    {
        "title": "Garlic Butter Paneer",
        "time": "15 min",
        "difficulty": "easy",
        "ingredients": ["Paneer", "Garlic", "Butter", "Salt", "Black Pepper"],
        "steps": [
            "Melt butter in a pan.",
            "Add minced garlic and sauté till fragrant.",
            "Add paneer cubes, salt, and pepper, cook until golden.",
            "Serve warm."
        ]
    },
    {
        "title": "Vegetable Stir Fry",
        "time": "25 min",
        "difficulty": "easy",
        "ingredients": ["Carrot", "Capsicum", "Peas", "Onion", "Garlic", "Soy Sauce", "Oil"],
        "steps": [
            "Heat oil in a wok.",
            "Add garlic and onion, sauté till translucent.",
            "Add chopped carrot, capsicum, and peas, stir fry for 10 min.",
            "Add soy sauce, mix well, serve hot."
        ]
    },
    {
        "title": "Spinach and Cheese Omelette",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Egg", "Spinach", "Cheese", "Salt", "Black Pepper", "Butter"],
        "steps": [
            "Beat eggs with salt and pepper.",
            "Melt butter in a pan, add spinach, cook 2 min.",
            "Pour eggs over spinach, sprinkle cheese on top.",
            "Cook until eggs are set, fold and serve."
        ]
    },
    {
        "title": "Lemon Yogurt Smoothie",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Yogurt", "Lemon", "Honey"],
        "steps": [
            "In a blender, combine yogurt, lemon juice, and honey.",
            "Blend until smooth.",
            "Serve chilled."
        ]
    },
    {
        "title": "Carrot and Peas Rice",
        "time": "30 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Carrot", "Peas", "Onion", "Garlic", "Salt", "Oil"],
        "steps": [
            "Cook rice and set aside.",
            "Heat oil, sauté onion and garlic.",
            "Add chopped carrot and peas, cook 5 min.",
            "Mix in rice, season with salt, serve hot."
        ]
    },
    {
        "title": "Butter Garlic Prawns",
        "time": "15 min",
        "difficulty": "easy",
        "ingredients": ["Prawn", "Garlic", "Butter", "Salt", "Black Pepper"],
        "steps": [
            "Melt butter in a pan.",
            "Add minced garlic, sauté till fragrant.",
            "Add prawns, salt, and pepper, cook until pink.",
            "Serve immediately."
        ]
    },
    {
        "title": "Cabbage Stir Fry",
        "time": "15 min",
        "difficulty": "easy",
        "ingredients": ["Cabbage", "Carrot", "Onion", "Soy Sauce", "Oil", "Salt"],
        "steps": [
            "Heat oil in a pan.",
            "Add onion, sauté till soft.",
            "Add chopped cabbage and carrot, cook for 8-10 min.",
            "Add soy sauce and salt, mix well, serve."
        ]
    },
    {
        "title": "Banana Milkshake",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Banana", "Milk", "Honey"],
        "steps": [
            "Combine banana, milk, and honey in a blender.",
            "Blend until smooth.",
            "Serve chilled."
        ]
    },
    {
        "title": "Tomato and Paneer Curry",
        "time": "25 min",
        "difficulty": "medium",
        "ingredients": ["Tomato", "Paneer", "Onion", "Garlic", "Ginger", "Salt", "Oil"],
        "steps": [
            "Heat oil in a pan.",
            "Add chopped onions, garlic, and ginger, sauté till golden.",
            "Add tomatoes, cook until soft.",
            "Add paneer cubes, salt, simmer 5 min.",
            "Serve hot with rice or bread."
        ]
    },
    {
        "title": "Mango Yogurt Smoothie",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Mango", "Yogurt", "Honey"],
        "steps": [
            "Peel and chop mango.",
            "Blend mango with yogurt and honey until smooth.",
            "Serve chilled."
        ]
    },
    {
        "title": "Egg Fried Rice",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Egg", "Onion", "Garlic", "Salt", "Oil"],
        "steps": [
            "Cook rice and set aside.",
            "Heat oil, sauté onions and garlic.",
            "Scramble eggs in the pan.",
            "Add rice, salt, mix well, and serve hot."
        ]
    },
    {
        "title": "Garlic Butter Chicken",
        "time": "30 min",
        "difficulty": "medium",
        "ingredients": ["Chicken", "Garlic", "Butter", "Salt", "Black Pepper"],
        "steps": [
            "Melt butter in a pan.",
            "Add minced garlic and sauté until fragrant.",
            "Add chicken, season with salt and pepper, cook until golden.",
            "Serve hot."
        ]
    },
    {
        "title": "Cucumber Salad",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Cucumber", "Tomato", "Salt", "Lemon"],
        "steps": [
            "Chop cucumber and tomatoes.",
            "Mix with salt and lemon juice.",
            "Serve fresh."
        ]
    },
    {
        "title": "Spiced Carrot Soup",
        "time": "25 min",
        "difficulty": "medium",
        "ingredients": ["Carrot", "Onion", "Garlic", "Salt", "Black Pepper", "Butter"],
        "steps": [
            "Sauté onions and garlic in butter until soft.",
            "Add chopped carrots and water, simmer until tender.",
            "Blend until smooth, season with salt and pepper, serve hot."
        ]
    },
    {
        "title": "Cheese and Spinach Sandwich",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Bread", "Spinach", "Cheese", "Butter", "Salt"],
        "steps": [
            "Butter the bread slices.",
            "Add spinach and cheese between slices.",
            "Grill until cheese melts and bread is golden."
        ]
    },
    {
        "title": "Paneer Stir Fry",
        "time": "20 min",
        "difficulty": "medium",
        "ingredients": ["Paneer", "Capsicum", "Onion", "Garlic", "Soy Sauce", "Oil"],
        "steps": [
            "Heat oil, sauté onion and garlic.",
            "Add capsicum and cook for 5 min.",
            "Add paneer cubes, soy sauce, cook until golden.",
            "Serve hot."
        ]
    },
    {
        "title": "Almond Milkshake",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Almonds", "Milk", "Honey"],
        "steps": [
            "Soak almonds for 2 hours and peel.",
            "Blend almonds with milk and honey until smooth.",
            "Serve chilled."
        ]
    },
    {
        "title": "Tomato Omelette",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Egg", "Tomato", "Onion", "Salt", "Black Pepper", "Butter"],
        "steps": [
            "Beat eggs with salt and pepper.",
            "Heat butter, sauté onion and tomato.",
            "Pour eggs over, cook until set, fold and serve."
        ]
    },
    {
        "title": "Lemon Rice",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Lemon", "Salt", "Oil"],
        "steps": [
            "Cook rice and set aside.",
            "Heat oil, add cooked rice, salt, and lemon juice.",
            "Mix well and serve hot."
        ]
    },
    {
        "title": "Vegetable Soup",
        "time": "25 min",
        "difficulty": "easy",
        "ingredients": ["Carrot", "Cabbage", "Peas", "Onion", "Garlic", "Salt", "Black Pepper", "Water"],
        "steps": [
            "Chop all vegetables.",
            "Boil water in a pot, add onions and garlic, cook until soft.",
            "Add carrots, cabbage, peas, and simmer for 10-15 min.",
            "Season with salt and pepper and serve hot."
        ]
    },
    {
        "title": "Butter Garlic Fish",
        "time": "20 min",
        "difficulty": "medium",
        "ingredients": ["Fish", "Garlic", "Butter", "Salt", "Black Pepper"],
        "steps": [
            "Melt butter in a pan.",
            "Add minced garlic and sauté until fragrant.",
            "Add fish fillets, season with salt and pepper, cook until golden.",
            "Serve immediately."
        ]
    },
    {
        "title": "Tomato and Cucumber Salad",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Tomato", "Cucumber", "Onion", "Salt", "Lemon"],
        "steps": [
            "Chop tomato, cucumber, and onion.",
            "Mix with salt and lemon juice.",
            "Serve fresh."
        ]
    },
    {
        "title": "Egg and Cheese Sandwich",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Bread", "Egg", "Cheese", "Butter", "Salt", "Black Pepper"],
        "steps": [
            "Butter the bread slices.",
            "Cook scrambled eggs with salt and pepper.",
            "Place eggs and cheese between bread slices and serve hot."
        ]
    },
    {
        "title": "Mutton Curry",
        "time": "45 min",
        "difficulty": "medium",
        "ingredients": ["Mutton", "Onion", "Garlic", "Ginger", "Salt", "Oil", "Turmeric", "Red Chili Powder"],
        "steps": [
            "Heat oil in a pan, sauté onions, garlic, and ginger until golden.",
            "Add mutton and cook until browned.",
            "Add spices, salt, and water, simmer for 30-35 min until mutton is tender.",
            "Serve hot with rice."
        ]
    },
    {
        "title": "Vegetable Pulao",
        "time": "30 min",
        "difficulty": "medium",
        "ingredients": ["Rice", "Carrot", "Peas", "Onion", "Garlic", "Oil", "Salt"],
        "steps": [
            "Cook rice and set aside.",
            "Heat oil, sauté onion and garlic.",
            "Add carrot and peas, cook for 5 min.",
            "Mix in rice and salt, cook for another 2 min, serve hot."
        ]
    },
    {
        "title": "Cashew Butter Spread",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Cashews", "Butter", "Salt"],
        "steps": [
            "Blend cashews with butter and a pinch of salt until smooth.",
            "Use as a spread for bread or crackers."
        ]
    },
    {
        "title": "Chicken Stir Fry",
        "time": "25 min",
        "difficulty": "medium",
        "ingredients": ["Chicken", "Capsicum", "Onion", "Garlic", "Soy Sauce", "Oil"],
        "steps": [
            "Heat oil in a pan, sauté garlic and onion.",
            "Add chicken pieces, cook until almost done.",
            "Add capsicum and soy sauce, cook 5 more min, serve hot."
        ]
    },
    {
        "title": "Spinach Paneer Curry",
        "time": "30 min",
        "difficulty": "medium",
        "ingredients": ["Spinach", "Paneer", "Onion", "Garlic", "Salt", "Oil"],
        "steps": [
            "Sauté onion and garlic in oil.",
            "Add chopped spinach, cook until wilted.",
            "Add paneer cubes, salt, and cook for 5 min, serve hot."
        ]
    },
    {
        "title": "Fruit Salad",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Apple", "Banana", "Mango", "Strawberry", "Lemon"],
        "steps": [
            "Chop all fruits into bite-size pieces.",
            "Mix with a squeeze of lemon juice.",
            "Serve fresh."
        ]
    },
    {
        "title": "Garlic Butter Almonds",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Almonds", "Garlic", "Butter", "Salt"],
        "steps": [
            "Melt butter in a pan, add minced garlic.",
            "Add almonds, toss for 5-7 min until golden.",
            "Season with salt and serve."
        ]
    },
    {
        "title": "Red Chili Chicken",
        "time": "35 min",
        "difficulty": "medium",
        "ingredients": ["Chicken", "Garlic", "Red Chili Powder", "Salt", "Oil"],
        "steps": [
            "Heat oil, sauté garlic until fragrant.",
            "Add chicken pieces, cook until lightly browned.",
            "Add red chili powder and salt, cook until chicken is done.",
            "Serve hot."
        ]
    },
    {
        "title": "Ginger Lemon Tea",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Ginger", "Lemon", "Water", "Honey"],
        "steps": [
            "Boil water with sliced ginger for 5-7 min.",
            "Add lemon juice and honey, stir well.",
            "Serve hot."
        ]
    },
    {
        "title": "Paneer Butter Masala",
        "time": "30 min",
        "difficulty": "medium",
        "ingredients": ["Paneer", "Tomato", "Butter", "Onion", "Garlic", "Salt", "Red Chili Powder"],
        "steps": [
            "Sauté onion and garlic in butter until golden.",
            "Add chopped tomatoes, cook until soft.",
            "Add paneer cubes, salt, red chili powder, simmer 5 min.",
            "Serve hot with rice or bread."
        ]
    },
    {
        "title": "Vegetable Rice Bowl",
        "time": "25 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Carrot", "Capsicum", "Peas", "Onion", "Soy Sauce", "Oil", "Salt"],
        "steps": [
            "Cook rice and set aside.",
            "Sauté onion in oil, add carrot, capsicum, and peas, cook 5-7 min.",
            "Add rice, soy sauce, salt, mix well, serve hot."
        ]
    },
    {
        "title": "Strawberry Yogurt Parfait",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Strawberry", "Yogurt", "Honey"],
        "steps": [
            "Layer yogurt and chopped strawberries in a glass.",
            "Drizzle honey on top.",
            "Serve chilled."
        ]
    },
    {
        "title": "Tomato Cabbage Stir Fry",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Tomato", "Cabbage", "Onion", "Garlic", "Salt", "Oil"],
        "steps": [
            "Heat oil, sauté onion and garlic.",
            "Add chopped cabbage and tomatoes, cook 10-12 min.",
            "Season with salt and serve hot."
        ]
    },
    {
        "title": "Cheesy Garlic Bread",
        "time": "15 min",
        "difficulty": "easy",
        "ingredients": ["Bread", "Butter", "Garlic", "Cheese", "Salt"],
        "steps": [
            "Mix butter with minced garlic and salt.",
            "Spread on bread slices, top with cheese.",
            "Bake until golden and cheese melts, serve hot."
        ]
    },
    {
        "title": "Spiced Vegetable Soup",
        "time": "25 min",
        "difficulty": "medium",
        "ingredients": ["Carrot", "Capsicum", "Peas", "Onion", "Garlic", "Salt", "Black Pepper", "Turmeric", "Water"],
        "steps": [
            "Sauté onion and garlic in oil.",
            "Add chopped vegetables and water, simmer until tender.",
            "Add salt, black pepper, and turmeric, cook 2 more min, serve hot."
        ]
    },
    {
        "title": "Mango and Strawberry Salad",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Mango", "Strawberry", "Lemon", "Honey"],
        "steps": [
            "Chop mango and strawberries.",
            "Mix with lemon juice and honey.",
            "Serve fresh."
        ]
    },
    {
        "title": "Cumin Spiced Rice",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Cumin", "Salt", "Oil"],
        "steps": [
            "Heat oil in a pan, add cumin seeds and sauté until fragrant.",
            "Add cooked rice and salt, mix well.",
            "Serve hot."
        ]
    },
    {
        "title": "Turmeric Chicken",
        "time": "35 min",
        "difficulty": "medium",
        "ingredients": ["Chicken", "Turmeric", "Garlic", "Salt", "Oil"],
        "steps": [
            "Heat oil, sauté garlic until fragrant.",
            "Add chicken and turmeric, cook until chicken is done.",
            "Season with salt and serve hot."
        ]
    },
    {
        "title": "Vegetable Omelette",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Egg", "Onion", "Capsicum", "Carrot", "Salt", "Black Pepper", "Butter"],
        "steps": [
            "Beat eggs with salt and pepper.",
            "Sauté chopped vegetables in butter.",
            "Pour eggs over vegetables, cook until set, fold and serve."
        ]
    },
    {
        "title": "Prawn Garlic Stir Fry",
        "time": "20 min",
        "difficulty": "medium",
        "ingredients": ["Prawn", "Garlic", "Oil", "Salt", "Black Pepper"],
        "steps": [
            "Heat oil, sauté minced garlic until fragrant.",
            "Add prawns, season with salt and pepper, cook until pink.",
            "Serve immediately."
        ]
    },
    {
        "title": "Ghee Rice",
        "time": "25 min",
        "difficulty": "easy",
        "ingredients": ["Rice", "Ghee", "Salt"],
        "steps": [
            "Cook rice and set aside.",
            "Heat ghee in a pan, add rice and salt, mix well.",
            "Serve hot."
        ]
    },
    {
        "title": "Cardamom Milk",
        "time": "10 min",
        "difficulty": "easy",
        "ingredients": ["Milk", "Cardamom", "Sugar"],
        "steps": [
            "Heat milk, add crushed cardamom and sugar.",
            "Simmer for 5 min, serve warm."
        ]
    },
    {
        "title": "Soy Sauce Vegetable Stir Fry",
        "time": "20 min",
        "difficulty": "easy",
        "ingredients": ["Carrot", "Capsicum", "Onion", "Peas", "Soy Sauce", "Oil", "Salt"],
        "steps": [
            "Heat oil, sauté onions until soft.",
            "Add other vegetables, cook for 5-7 min.",
            "Add soy sauce and salt, stir well, serve hot."
        ]
    },
    {
        "title": "Butter Toast",
        "time": "5 min",
        "difficulty": "easy",
        "ingredients": ["Bread", "Butter", "Salt"],
        "steps": [
            "Spread butter and a pinch of salt on bread slices.",
            "Toast until golden brown.",
            "Serve warm."
        ]
    },
    {
        "title": "Cashew Rice",
        "time": "25 min",
        "difficulty": "medium",
        "ingredients": ["Rice", "Cashews", "Oil", "Salt"],
        "steps": [
            "Heat oil, roast cashews until golden.",
            "Add cooked rice and salt, mix well.",
            "Serve hot."
        ]
    },
    {
        "title": "Black Pepper Chicken",
        "time": "30 min",
        "difficulty": "medium",
        "ingredients": ["Chicken", "Black Pepper", "Garlic", "Salt", "Oil"],
        "steps": [
            "Heat oil, sauté garlic until fragrant.",
            "Add chicken, salt, and black pepper.",
            "Cook until chicken is golden and cooked through.",
            "Serve hot."
        ]
    } 
]

    # --- Create Recipes ---
    for r in recipe_data:
        recipe, _ = Recipe.objects.get_or_create(
            title=r["title"],
            defaults={
                "time": r["time"],
                "difficulty": r["difficulty"],
                "steps": r["steps"]
            }
        )

        if not recipe.slug:
            recipe.slug = generate_unique_slug(recipe)
            recipe.save()

        recipe_ingredients = []
        for ing_name in r["ingredients"]:
            ing = ingredients.get(ing_name)
            if not ing:
                # Auto-create missing ingredient in Spices category
                ing = Ingredient.objects.create(name=ing_name, category=categories.get("Spices"))
                ingredients[ing_name] = ing
            recipe_ingredients.append(ing)

        recipe.ingredients.set(recipe_ingredients)

    print(f"✅ Created {len(recipe_data)} recipes")
    print("🌿 Manual seed complete! Database is ready.")
