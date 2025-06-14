from db import mysql

def get_adventures_by_location(location):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM adventures WHERE location = %s"
    cursor.execute(query, (location,))
    data = cursor.fetchall()
    cursor.close()
    return data
