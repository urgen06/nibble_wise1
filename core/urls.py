from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('recipes/', views.recipes, name='recipes'),
    path('about/', views.about, name='about'),
    path('recipes/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),

]