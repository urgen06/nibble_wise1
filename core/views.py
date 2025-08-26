from django.shortcuts import render


def home(request):
    ingredients = [
        {"name": "Tomato", "category": "Vegetable", "image": "images/tomato.jpg"},
        {"name": "Onion", "category": "Vegetable", "image": "images/onion.jpg"},
        {"name": "Egg", "category": "Protein", "image": "images/egg.jpg"},
        {"name": "Milk", "category": "Dairy", "image": "images/milk.jpg"},
    ]
    return render(request, 'home.html', {"ingredients": ingredients})


def ingredients(request):
    ingredients = [
        {"name": "Tomato", "category": "Vegetable", "image": "images/tomato.jpg"},
        {"name": "Onion", "category": "Vegetable", "image": "images/onion.jpg"},
        {"name": "Egg", "category": "Protein", "image": "images/egg.jpg"},
        {"name": "Milk", "category": "Dairy", "image": "images/milk.jpg"},
        {"name": "Chicken", "category": "Protein", "image": "images/chicken.jpg"},
        {"name": "Spinach", "category": "Vegetable", "image": "images/spinach.jpg"},
        {"name": "Cheese", "category": "Dairy", "image": "images/cheese.jpg"},
        {"name": "Garlic", "category": "Vegetable", "image": "images/garlic.jpg"},
    ]
    categories = sorted({i["category"] for i in ingredients})
    return render(request, 'ingredients.html', {"ingredients": ingredients, "categories": categories})


def recipes(request):
    recipes = [
        {
            "slug": "tomato-omelette",
            "title": "Tomato Omelette",
            "time": 15,
            "difficulty": "Easy",
            "popularity": 87,
            "image": "images/recipe1.jpg",
        },
        {
            "slug": "creamy-garlic-chicken",
            "title": "Creamy Garlic Chicken",
            "time": 35,
            "difficulty": "Medium",
            "popularity": 95,
            "image": "images/recipe2.jpg",
        },
        {
            "slug": "spinach-cheese-quiche",
            "title": "Spinach & Cheese Quiche",
            "time": 50,
            "difficulty": "Hard",
            "popularity": 72,
            "image": "images/recipe3.jpg",
        },
    ]
    return render(request, 'recipes.html', {"recipes": recipes})


def recipe_detail(request, slug):
    recipe = {
        "slug": slug,
        "title": slug.replace('-', ' ').title(),
        "time": 30,
        "difficulty": "Medium",
        "image": "images/recipe1.jpg",
        "ingredients": ["Tomato", "Egg", "Onion", "Garlic"],
        "steps": [
            "Chop ingredients.",
            "Heat pan and cook.",
            "Serve hot.",
        ],
    }
    return render(request, 'recipe_detail.html', {"recipe": recipe})


def about(request):
    return render(request, 'about.html')
