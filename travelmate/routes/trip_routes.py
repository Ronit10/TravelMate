from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.trip_model import create_trip, find_matching_travelers

trip_bp = Blueprint("trip", __name__)

# Create Trip
@trip_bp.route("/trip", methods=["POST"])
@jwt_required()
def create_trip_route():
    user_id = get_jwt_identity()
    data = request.json
    return create_trip(user_id, data["destination"], data["start_date"], data["end_date"], data["budget"], data["travel_type"])

# Get Matching Travelers
@trip_bp.route("/match", methods=["GET"])
@jwt_required()
def get_matching_travelers():
    destination = request.args.get("destination")
    budget_min = float(request.args.get("budget_min", 0))
    budget_max = float(request.args.get("budget_max", 100000))
    travel_type = request.args.get("travel_type", "Solo")

    matches = find_matching_travelers(destination, (budget_min, budget_max), travel_type)
    return jsonify({"matches": matches}), 200
