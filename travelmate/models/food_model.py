from db import mysql

def get_food_by_location(location):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM food WHERE available_in_location = %s"
    cursor.execute(query, (location,))
    data = cursor.fetchall()
    cursor.close()
    return data
