from flask import Blueprint, request, jsonify
from config import mysql

cost_bp = Blueprint('cost', __name__)

@cost_bp.route('/cost/estimate', methods=['GET'])
def estimate_cost():
    location = request.args.get('location')
    if not location:
        return jsonify({"success": False, "message": "❌ Location is required"}), 400

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT AVG(price) FROM hotels WHERE location = %s", (location,))
        hotel_cost = cursor.fetchone()[0] or 0

        cursor.execute("SELECT AVG(price) FROM food WHERE location = %s", (location,))
        food_cost = cursor.fetchone()[0] or 0

        cursor.execute("SELECT AVG(price) FROM adventures WHERE location = %s", (location,))
        adventure_cost = cursor.fetchone()[0] or 0

        cursor.close()

        total = hotel_cost + food_cost + adventure_cost

        return jsonify({
            "success": True,
            "location": location,
            "hotel": round(hotel_cost, 2),
            "food": round(food_cost, 2),
            "adventure": round(adventure_cost, 2),
            "total": round(total, 2)
        })
    except Exception as e:
        print("Cost Estimation Error:", str(e))
        return jsonify({"success": False, "message": "Something went wrong while estimating cost."}), 500
