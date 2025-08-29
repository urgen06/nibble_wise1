from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category,Ingredient,Recipe

from django.db.models import Q
import requests
from django.http import JsonResponse
from urllib.parse import quote


@login_required(login_url='login')
def api_recipe_detail(request, title):
    API_KEY = "F5kjAeW8WuQIvS2b8tF7oA==fjAB5c17MRec7i2q"
    query = quote(title)
    url = f"https://api.api-ninjas.com/v1/recipe?query={query}"
    headers = {"X-Api-Key": API_KEY}

    recipe = {}
    ingredients_list = []

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                recipe = data[0]
                ingredients_list = recipe.get("ingredients", "").split("|") if recipe.get("ingredients") else []
        else:
            print("API Error:", response.status_code, response.text)
    except requests.RequestException as e:
        print("Request Exception:", e)

    return render(request, "api_recipe_detail.html", {
        "recipe": recipe,
        "ingredients_list": ingredients_list
    })


@login_required(login_url='login')
def suggest_recipes(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({"error": "Please enter at least one ingredient."}, status=400)

    # ------------------- DB Recipes -------------------
    db_recipes = Recipe.objects.filter(
        ingredients__name__icontains=query
    ).distinct()

    db_results = []
    for r in db_recipes:
        db_results.append({
            "title": r.title,
            "slug": r.slug,
            "time": r.time,
            "difficulty": r.difficulty,
            "photos": [p.url for p in r.photos()]  # using your photos() helper
        })

    # ------------------- API Recipes -------------------
    API_KEY = "F5kjAeW8WuQIvS2b8tF7oA==fjAB5c17MRec7i2q" 
    url = f"https://api.api-ninjas.com/v1/recipe?query={query}"
    headers = {"X-Api-Key": API_KEY}

    api_results = []
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        print("Status:", response.status_code)
        print(response.json())

        if response.status_code == 200:
            data = response.json()
            for r in data:
                api_results.append({
                    "title": r.get("title", "No Title"),
                    "ingredients": r.get("ingredients", "No ingredients provided."),
                    "instructions": r.get("instructions", "No instructions provided.")
                })
    except requests.RequestException:
        pass

    # ------------------- Combine -------------------
    combined_results = {
        "db_recipes": db_results,
        "api_recipes": api_results
    }

    return JsonResponse(combined_results, safe=False)

# ------------------- Signup -------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'signup.html')

# ------------------- Login -------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to homepage
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

# ------------------- Logout -------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------- Homepage -------------------
def home(request):
    ingredients = [
        {"name": "Tomato", "category": "Vegetable", "image": "images/tomato.jpg"},
        {"name": "Onion", "category": "Vegetable", "image": "images/onion.jpg"},
        {"name": "Egg", "category": "Protein", "image": "images/egg.jpg"},
        {"name": "Milk", "category": "Dairy", "image": "images/milk.jpg"},
    ]
    return render(request, 'home.html', {"ingredients": ingredients})

# ------------------- Ingredients Page -------------------
@login_required(login_url='login')
def ingredients(request):
    
    ingredients = Ingredient.objects.select_related('category').all()

    categories = Category.objects.all().order_by('name')

    return render(request, 'ingredients.html', {
        "ingredients": ingredients,
        "categories": categories
    })

# ------------------- Recipes Page -------------------
@login_required(login_url='login')
def recipes(request):
    recipes = Recipe.objects.all()
    # recipes = [
    #     {
    #         "slug": "tomato-omelette",
    #         "title": "Tomato Omelette",
    #         "time": 15,
    #         "difficulty": "Easy",
    #         "popularity": 87,
    #         "image": "images/recipe1.jpg",
    #     },
    #     {
    #         "slug": "creamy-garlic-chicken",
    #         "title": "Creamy Garlic Chicken",
    #         "time": 35,
    #         "difficulty": "Medium",
    #         "popularity": 95,
    #         "image": "images/recipe2.jpg",
    #     },
    #     {
    #         "slug": "spinach-cheese-quiche",
    #         "title": "Spinach & Cheese Quiche",
    #         "time": 50,
    #         "difficulty": "Hard",
    #         "popularity": 72,
    #         "image": "images/recipe3.jpg",
    #     },
    # ]
    return render(request, 'recipes.html', {"recipes": recipes})

# ------------------- Recipe Detail -------------------
@login_required(login_url='login')
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipe_detail.html', {"recipe": recipe})

# ------------------- About -------------------
def about(request):
    return render(request, 'about.html')
