from flask import Blueprint, request, jsonify
from models.hotel_model import get_hotels_by_location

hotel_bp = Blueprint("hotel", __name__)

@hotel_bp.route("/hotels", methods=["GET"])
def fetch_hotels():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    hotels = get_hotels_by_location(location)
    return jsonify({"hotels": hotels}), 200
