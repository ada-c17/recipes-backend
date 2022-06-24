from flask import Blueprint, json, jsonify, request, abort, make_response
import os
import requests

def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))
        
    obj = cls.query.get(id)
    
    if not obj:
        return abort(make_response({"message": f"{cls} {id} not found"}, 404))

    return obj

def get_spoonacular_desserts():
    PATH = "https://api.spoonacular.com/recipes/random?limitLicense=true&tags=dessert&number=10"
    API_KEY = os.environ.get("SPOONACULAR_KEY")
    query_params = {
        "apiKey": API_KEY,
        "format": "json"
    }
    response = requests.get(PATH, params=query_params)
    recipes_list = []
    for recipe in response.json()["recipes"]:
        recipe_dict = {}
        ingredients_list = []
        recipe_dict["name"] = recipe["title"]
        for ing in recipe["extendedIngredients"]:
            ingredients_list.append(ing["original"])

        ingredients_str = ",".join(ingredients_list)
        recipe_dict["ingredients"] = ingredients_str
        recipes_list.append(recipe_dict)
    return recipes_list