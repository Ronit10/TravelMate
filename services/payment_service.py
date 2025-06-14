from flask import jsonify
from app import mysql

# Process Payment
def process_payment(user_id, booking_id, amount, method):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Payments (user_id, booking_id, amount, payment_method, status) VALUES (%s, %s, %s, %s, 'Success')",
        (user_id, booking_id, amount, method))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Payment successful!"}), 200
