from flask import Blueprint, request, jsonify
from models.food_model import get_food_by_location

food_bp = Blueprint("food", __name__)

@food_bp.route("/foods", methods=["GET"])
def get_foods():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    foods = get_food_by_location(location)
    return jsonify({"foods": foods}), 200
