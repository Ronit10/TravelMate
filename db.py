from flask_mysqldb import MySQL 

mysql = MySQL()

def get_connection():
    return mysql.connection
