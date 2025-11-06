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

from .recommendations import content_based_recipes, collaborative_recipes

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



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
    # 1️⃣ Get ingredients from ?ingredients=... or ?q=...
    ingredients_list = request.GET.getlist('ingredients')
    if not ingredients_list:
        q = request.GET.get('q', '').strip()
        if q:
            # Split by comma or space
            ingredients_list = [i.strip() for i in q.replace(',', ' ').split()]

    if not ingredients_list:
        return JsonResponse({"error": "Please select at least one ingredient."}, status=400)

    # 2️⃣ Build OR query for all ingredients
    query = Q()
    for ing in ingredients_list:
        query |= Q(ingredients__name__icontains=ing)

    db_recipes = Recipe.objects.filter(query).distinct()

    # 3️⃣ Prepare DB recipes result
    db_results = [{
        "title": r.title,
        "slug": r.slug,
        "time": r.time,
        "difficulty": r.difficulty,
        "photos": [p.url for p in getattr(r, 'photos', lambda: [])()]
    } for r in db_recipes]

    # 4️⃣ Content-based and collaborative recommendations
    content_results = content_based_recipes(ingredients_list)
    collaborative_results = collaborative_recipes(request.user)

    # 5️⃣ Print debug info before returning
    print("DB:", db_results)
    print("Content-Based:", content_results)
    print("Collaborative:", collaborative_results)

    # 6️⃣ Add sample data if missing (for testing)
    if not content_results:
        content_results = [
        {"slug": "sample-content", "title": "Sample Content Recipe"}
    ]

    if not collaborative_results:
        collaborative_results = [
        {"slug": "sample-collab", "title": "Sample Collaborative Recipe"}
    ]

    # 7️⃣ Finally, return the JSON response
    return JsonResponse({
        "db_recipes": db_results,
        "content_based": content_results,
        "collaborative": collaborative_results
    }, safe=False)



@login_required(login_url='login')
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    all_recipes = Recipe.objects.exclude(id=recipe.id)
    
    # ✅ Get similar recipes
    similar_recipes = get_similar_recipes(recipe, all_recipes)

    return render(request, 'recipe_detail.html', {
        "recipe": recipe,
        "similar_recipes": similar_recipes
    })


# -------- Content based filtering--------
def get_similar_recipes(target_recipe, all_recipes):
    # Convert QuerySet to list so it supports indexing
    all_recipes = list(all_recipes)

    # Convert ingredient objects into plain text
    def join_ingredients(recipe):
        return " ".join(i.name for i in recipe.ingredients.all())

    # Prepare TF-IDF corpus
    corpus = [join_ingredients(r) for r in all_recipes]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Target recipe vector
    target_vec = vectorizer.transform([join_ingredients(target_recipe)])
    cosine_sim = cosine_similarity(target_vec, tfidf_matrix).flatten()

    # Get top similar recipes (highest similarity scores)
    top_indices = cosine_sim.argsort()[-5:][::-1]

    # ✅ Convert NumPy int64 indices to Python int and ensure unique recipe
    similar_recipes = [
        all_recipes[int(i)] for i in top_indices
        if all_recipes[int(i)].id != target_recipe.id
    ]
    return similar_recipes[:5]


def join_ingredients(recipe):
    return f"{recipe.title} " + " ".join(i.name for i in recipe.ingredients.all())

# @login_required(login_url='login')
# def suggest_recipes(request):
#     query = request.GET.get('q', '').strip()

#     if not query:
#         return JsonResponse({"error": "Please enter at least one ingredient."}, status=400)

#     # ------------------- DB Recipes -------------------
#     db_recipes = Recipe.objects.filter(
#         ingredients__name__icontains=query
#     ).distinct()

#     db_results = []
#     for r in db_recipes:
#         db_results.append({
#             "title": r.title,
#             "slug": r.slug,
#             "time": r.time,
#             "difficulty": r.difficulty,
#             "photos": [p.url for p in r.photos()]  # using your photos() helper
#         })

# @login_required(login_url='login')
# def suggest_recipes(request):
#     # 1️⃣ Get ingredients from GET parameters
#     # Supports ?ingredients=Tomato&ingredients=Onion
#     ingredients_query = request.GET.getlist('ingredients')

#     # Or supports ?q=Tomato,Onion (comma or space separated)
#     if not ingredients_query:
#         q = request.GET.get('q', '').strip()
#         if q:
#             # Replace commas with spaces, then split by space
#             ingredients_query = [i.strip() for i in q.replace(',', ' ').split() if i.strip()]

#     if not ingredients_query:
#         return JsonResponse({"error": "Please select at least one ingredient."}, status=400)

#     # 2️⃣ Filter recipes containing ALL selected ingredients
#     db_recipes = Recipe.objects.all()
#     for ingredient_name in ingredients_query:
#         db_recipes = db_recipes.filter(ingredients__name__icontains=ingredient_name)
#     db_recipes = db_recipes.distinct()

#     # 3️⃣ Prepare JSON response
#     db_results = []
#     for r in db_recipes:
#         db_results.append({
#             "title": r.title,
#             "slug": r.slug,
#             "time": r.time,
#             "difficulty": r.difficulty,
#             "photos": [p.url for p in getattr(r, 'photos', lambda: [])()]  # safe fallback
#         })

#     return JsonResponse({"db_recipes": db_results}, safe=False)



    # ------------------- API Recipes -------------------
    # API_KEY = "F5kjAeW8WuQIvS2b8tF7oA==fjAB5c17MRec7i2q" 
    # url = f"https://api.api-ninjas.com/v1/recipe?query={query}"
    # headers = {"X-Api-Key": API_KEY}

    # api_results = []
    # try:
    #     response = requests.get(url, headers=headers, timeout=5)
        
    #     print("Status:", response.status_code)
    #     print(response.json())

    #     if response.status_code == 200:
    #         data = response.json()
    #         for r in data:
    #             api_results.append({
    #                 "title": r.get("title", "No Title"),
    #                 "ingredients": r.get("ingredients", "No ingredients provided."),
    #                 "instructions": r.get("instructions", "No instructions provided.")
    #             })
    # except requests.RequestException:
    #     pass

    # # ------------------- Combine -------------------
    # combined_results = {
    #     "db_recipes": db_results,
    #     "api_recipes": api_results
    # }

    # return JsonResponse(combined_results, safe=False)

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


# ------------------- About -------------------
def about(request):
    return render(request, 'about.html')


