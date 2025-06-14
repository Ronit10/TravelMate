import os

MYSQL_HOST = "mysql-1234.railway.internal"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Abcd1234"
MYSQL_DB = "travelmate"
JWT_SECRET_KEY = "3306" 
from flask_mysqldb import MySQL

mysql = MySQL()
