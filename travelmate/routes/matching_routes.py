from flask import Blueprint, request, jsonify
from config import mysql
from datetime import datetime

matching_bp = Blueprint('matching', __name__)

# Route to create a new trip for a user
@matching_bp.route('/trip/create', methods=['POST'])
def create_trip():
    try:
        user_id = request.form['user_id']
        destination = request.form['destination']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = request.form['budget']
        travel_type = request.form['travel_type']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO trip (user_id, destination, start_date, end_date, budget, travel_type, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, destination, start_date, end_date, budget, travel_type, datetime.now()))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Trip created successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Trip creation failed: {str(e)}"})


# Route to search matching trips by location and date
@matching_bp.route('/trip/search', methods=['GET'])
def search_trips():
    try:
        destination = request.args.get('destination')
        start_date = request.args.get('start_date')

        cursor = mysql.connection.cursor()
        query = """
            SELECT t.trip_id, t.user_id, t.destination, t.start_date, t.end_date, t.budget, t.travel_type, t.created_at, u.name, u.email 
            FROM trip t
            JOIN users u ON t.user_id = u.id
            WHERE t.destination = %s AND t.start_date = %s
        """
        cursor.execute(query, (destination, start_date))
        results = cursor.fetchall()

        trips = []
        for row in results:
            trips.append({
                "trip_id": row[0],
                "user_id": row[1],
                "destination": row[2],
                "start_date": str(row[3]),
                "end_date": str(row[4]),
                "budget": row[5],
                "travel_type": row[6],
                "created_at": str(row[7]),
                "name": row[8],
                "email": row[9]
            })

        return jsonify({"success": True, "trips": trips})
    except Exception as e:
        return jsonify({"success": False, "message": f"Search failed: {str(e)}"})
