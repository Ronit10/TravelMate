from flask import jsonify
from db import mysql

# Create Trip
def create_trip(user_id, destination, start_date, end_date, budget, travel_type):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Trips (user_id, destination, start_date, end_date, budget, travel_type) VALUES (%s, %s, %s, %s, %s, %s)", 
        (user_id, destination, start_date, end_date, budget, travel_type))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Trip created successfully!"}), 201

# Get Matching Travelers
def find_matching_travelers(destination, budget_range, travel_type):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT user_id, name FROM Users WHERE user_id IN "
        "(SELECT user_id FROM Trips WHERE destination = %s AND travel_type = %s AND budget BETWEEN %s AND %s)", 
        (destination, travel_type, budget_range[0], budget_range[1]))
    travelers = cursor.fetchall()
    cursor.close()
    
    return [{"user_id": t[0], "name": t[1]} for t in travelers]
