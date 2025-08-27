from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

# ------------------- Recipes Page -------------------
@login_required(login_url='login')
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

# ------------------- Recipe Detail -------------------
@login_required(login_url='login')
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

# ------------------- About -------------------
def about(request):
    return render(request, 'about.html')
