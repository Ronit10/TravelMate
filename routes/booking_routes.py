from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.booking_model import create_booking, get_user_bookings

booking_bp = Blueprint("booking", __name__)

# Create a Booking (Hotel, Flight, Adventure)
@booking_bp.route("/booking", methods=["POST"])
@jwt_required()
def create_booking_route():
    user_id = get_jwt_identity()
    data = request.json
    return create_booking(user_id, data["trip_id"], data["booking_type"], data["details"], data["amount"])

# Get User's Bookings
@booking_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = get_jwt_identity()
    bookings = get_user_bookings(user_id)
    return jsonify({"bookings": bookings}), 200
