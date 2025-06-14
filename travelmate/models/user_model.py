from db import get_connection
import MySQLdb.cursors

def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password))

    conn.commit()

    cursor.close()
    return {"message": "User created successfully"}, 201

def get_user(email):
    from app import mysql
    import MySQLdb.cursors

    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)  # DictCursor very important!
        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print("Error in get_user:", e)
        return None
    finally:
        cursor.close()

