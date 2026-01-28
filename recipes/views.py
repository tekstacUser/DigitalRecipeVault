from django.shortcuts import render, redirect
from django.contrib import messages
from bson import ObjectId

from .models import UserMongo, RecipeMongo
from .forms import UserForm, RecipeForm


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            # Check already exists
            existing = UserMongo.get_user_by_email(email)
            if existing:
                messages.error(request, "Email already exists!")
                return redirect("register")

            UserMongo.create_user(name, email)
            messages.success(request, "Registration Successful!")
            return redirect("login")
    else:
        form = UserForm()

    return render(request, "register.html", {"form": form})


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = UserMongo.get_user_by_email(email)
        if user:
            request.session["user_id"] = user["id"]
            request.session["user_name"] = user["name"]
            return redirect("recipe_list")
        else:
            messages.error(request, "Invalid Email")

    return render(request, "login.html")


def logout(request):
    request.session.flush()
    return redirect("login")


def recipe_list(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    query = request.GET.get("q", "").strip()
    tag_filter = request.GET.get("tag", "").strip()

    recipes = RecipeMongo.get_recipes_by_user(user_id)

    # Manual search using python filter
    if query:
        recipes = [
            r for r in recipes
            if query.lower() in r.get("title", "").lower()
            or any(query.lower() in ing.lower() for ing in r.get("ingredients", []))
        ]

    if tag_filter:
        recipes = [
            r for r in recipes
            if tag_filter.lower() in [t.lower() for t in r.get("tags", [])]
        ]

    user = {
        "id": user_id,
        "name": request.session.get("user_name", "")
    }

    return render(request, "recipe_list.html", {"recipes": recipes, "user": user})


def add_recipe(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            ingredients = [i.strip() for i in form.cleaned_data["ingredients"].split(",") if i.strip()]
            steps = [s.strip() for s in form.cleaned_data["steps"].split(",") if s.strip()]
            tags = [t.strip() for t in form.cleaned_data["tags"].split(",") if t.strip()] if form.cleaned_data.get("tags") else []

            RecipeMongo.create_recipe(
                user_id=user_id,
                title=title, 
                ingredients_list=ingredients, 
                steps_list=steps,
                tags_list=tags
            )

            messages.success(request, "Recipe Added Successfully!")
            return redirect("recipe_list")
    else:
        form = RecipeForm()

    return render(request, "add_recipe.html", {"form": form})


def edit_recipe(request, pk):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    recipe = RecipeMongo.get_recipe_by_id(pk)
    if not recipe:
        messages.error(request, "Recipe not found!")
        return redirect("recipe_list")

    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            ingredients = [i.strip() for i in form.cleaned_data["ingredients"].split(",") if i.strip()]
            steps = [s.strip() for s in form.cleaned_data["steps"].split(",") if s.strip()]
            tags = [t.strip() for t in form.cleaned_data["tags"].split(",") if t.strip()] if form.cleaned_data.get("tags") else []

            RecipeMongo.update_recipe(
                recipe_id=pk,
                title=title,
                ingredients=ingredients,
                steps=steps,
                tags=tags
            )

            messages.success(request, "Recipe Updated Successfully!")
            return redirect("recipe_list")
    else:
        # Pre-fill data in form
        form = RecipeForm(initial={
            "title": recipe.get("title", ""),
            "ingredients": ", ".join(recipe.get("ingredients", [])),
            "steps": ", ".join(recipe.get("steps", [])),
            "tags": ", ".join(recipe.get("tags", [])),
        })

    return render(request, "edit_recipe.html", {"form": form, "recipe": recipe})

def delete_recipe(request, pk): 
    recipe = RecipeMongo.get_recipe_by_id(pk)
    if not recipe:
        messages.error(request, "Recipe not found!")
        return redirect("recipe_list")

    if request.method == "POST":
        RecipeMongo.delete_recipe(pk)
        messages.success(request, "Recipe Deleted Successfully!")
        return redirect("recipe_list")

    return render(request, "delete_recipe.html", {"recipe": recipe})
