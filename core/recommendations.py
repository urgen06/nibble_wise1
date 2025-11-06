from django.db.models import Count
from .models import Recipe, UserRecipe, Ingredient
from django.contrib.auth.models import User

# ----------------- Content-Based Filtering -----------------
def content_based_recipes(ingredients_query):
    """
    Return recipes sorted by number of matching ingredients.
    ingredients_query: list of ingredient names
    """
    if not ingredients_query:
        return []

    recipes = Recipe.objects.filter(ingredients__name__in=ingredients_query).distinct()
    recipes = recipes.annotate(shared_ingredients=Count('ingredients')).order_by('-shared_ingredients')

    results = []
    for r in recipes:
        results.append({
            "title": r.title,
            "slug": r.slug,
            "time": r.time,
            "difficulty": r.difficulty,
            "shared_ingredients": r.shared_ingredients,
        })
    return results


# ----------------- Collaborative Filtering -----------------
def collaborative_recipes(user):
    """
    Recommend recipes based on what other users with similar tastes liked.
    """
    if not user.is_authenticated:
        return []

    # Recipes the user has viewed or liked
    user_recipes = UserRecipe.objects.filter(user=user).values_list('recipe', flat=True)

    # Users who liked the same recipes
    similar_users = UserRecipe.objects.filter(recipe__in=user_recipes).exclude(user=user).values_list('user', flat=True)

    # Recipes these users liked that the current user hasn't seen
    recommended = UserRecipe.objects.filter(user__in=similar_users).exclude(recipe__in=user_recipes)
    recommended = recommended.values('recipe__title', 'recipe__slug').annotate(count=Count('recipe')).order_by('-count')

    results = []
    for r in recommended:
        results.append({
            "title": r['recipe__title'],
            "slug": r['recipe__slug'],
            "popularity": r['count']
        })
    return results
