from flask import Blueprint, request, jsonify
from models.adventure_model import get_adventures_by_location

adventure_bp = Blueprint("adventure", __name__)

@adventure_bp.route("/adventures", methods=["GET"])
def get_adventures():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    adventures = get_adventures_by_location(location)
    return jsonify({"adventures": adventures}), 200
