# recipevault/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),
    path("edit/<str:pk>/", views.edit_recipe, name="edit_recipe"),
    path("delete/<str:pk>/", views.delete_recipe, name="delete_recipe"),

]
