from db import mysql

def get_hotels_by_location(location):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM hotels WHERE location = %s"
    cursor.execute(query, (location,))
    hotels = cursor.fetchall()
    cursor.close()
    return hotels
