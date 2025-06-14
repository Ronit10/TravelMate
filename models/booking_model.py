from flask import jsonify
from db import mysql

# Create Booking (Hotel, Flight, Activity)
def create_booking(user_id, trip_id, booking_type, details, amount):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Bookings (user_id, trip_id, booking_type, details, amount) VALUES (%s, %s, %s, %s, %s)", 
        (user_id, trip_id, booking_type, details, amount))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Booking created successfully!"}), 201

# Get User's Bookings
def get_user_bookings(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT booking_id, booking_type, details, amount, status FROM Bookings WHERE user_id = %s", (user_id,))
    bookings = cursor.fetchall()
    cursor.close()
    
    return [{"booking_id": b[0], "type": b[1], "details": b[2], "amount": b[3], "status": b[4]} for b in bookings]
