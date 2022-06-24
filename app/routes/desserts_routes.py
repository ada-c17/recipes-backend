from flask import Blueprint, json, jsonify, request
from app.models.dessert import Dessert
from app.routes.helper_routes import validate_record, get_spoonacular_desserts
from app import db

desserts_bp = Blueprint("desserts_bp", __name__, url_prefix="/desserts")

@desserts_bp.route("/s", methods=["POST"])
def seed_dessert():
    recipes = get_spoonacular_desserts()
    for recipe in recipes:
        new_dessert = Dessert.create(recipe)
        print(new_dessert)
        db.session.add(new_dessert)
    db.session.commit()

    return jsonify(f"{len(recipes)} have been successfully created"), 201
    

@desserts_bp.route("", methods=["POST"])
def create_dessert():
    request_body = request.get_json()

    # guard clause
    if "name" not in request_body or "ingredients" not in request_body:
        return jsonify("Invalid Request"), 400

    new_dessert = Dessert.create(request_body)

    db.session.add(new_dessert)
    db.session.commit()
    
    return jsonify(f"{new_dessert.name} has been successfully created"), 201

@desserts_bp.route("", methods=["GET"])
def read_all_desserts():
    desserts = Dessert.query.all()
    desserts_response = [ dessert.to_json() for dessert in desserts]
    print(desserts)
    return jsonify(desserts_response), 200

@desserts_bp.route("/<id>", methods=["GET"])
def read_one_dessert(id):
    dessert = validate_record(Dessert, id)
    return dessert.to_dict()

@desserts_bp.route("/<id>", methods=["PUT"])
def update_one_dessert(id):
    dessert = validate_record(Dessert, id)
    request_body = request.get_json()
    dessert.update(request_body)
    db.session.commit()
    return jsonify(f"Dessert {dessert.id} successfully updated"), 200

@desserts_bp.route("/<id>", methods=["DELETE"])
def delete_one_dessert(id):
    dessert = validate_record(Dessert, id)
    db.session.delete(dessert)
    db.session.commit()
    return jsonify(f"Dessert {dessert.id} successfully deleted"), 200

