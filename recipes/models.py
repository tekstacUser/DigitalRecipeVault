from bson import ObjectId
from .mongo_db import users_collection, recipes_collection


class UserMongo:
    @staticmethod
    def create_user(name, email):
        user_data = {
            "name": name,
            "email": email
        }
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_email(email):
        user = users_collection.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user

    @staticmethod
    def get_user_by_id(user_id):
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user


class RecipeMongo:
    @staticmethod
    def create_recipe(user_id, title, ingredients_list, steps_list, tags_list=None):
        recipe_data = {
            "user_id": ObjectId(user_id) if user_id else None,
            "title": title,
            "ingredients": ingredients_list,
            "steps": steps_list,
            "tags": tags_list if tags_list else [],
        }
        result = recipes_collection.insert_one(recipe_data)
        return str(result.inserted_id)

    @staticmethod
    def get_recipe_by_id(recipe_id):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe:
            recipe["id"] = str(recipe["_id"])
            del recipe["_id"]

            if recipe.get("user_id"):
                recipe["user_id"] = str(recipe["user_id"])
        return recipe

    @staticmethod
    def get_recipes_by_user(user_id):
        recipes = list(recipes_collection.find({"user_id": ObjectId(user_id)}))
        for r in recipes:
            r["id"] = str(r["_id"])
            del r["_id"]

            if r.get("user_id"):
                r["user_id"] = str(r["user_id"])
        return recipes

    @staticmethod
    def update_recipe(recipe_id, title, ingredients, steps, tags):
        recipes_collection.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$set": {
                "title": title,
                "ingredients": ingredients,
                "steps": steps,
                "tags": tags
            }}
        )

    @staticmethod
    def delete_recipe(recipe_id):
        recipes_collection.delete_one({"_id": ObjectId(recipe_id)})
