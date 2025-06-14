from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config
from db import mysql, get_connection  
from routes.hotel_routes import hotel_bp
from routes.food_routes import food_bp
from routes.adventure_routes import adventure_bp
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from routes.chat_routes import chat_bp
from routes.matching_routes import matching_bp
from routes.cost_routes import cost_bp
from config import mysql

app = Flask(__name__)
CORS(app)

# MySQL Config
app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql.init_app(app)  # ✅ Important line

# JWT Config
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

# ✅ Blueprint Registration
def register_blueprints():
    from routes.auth_routes import auth_bp
    from routes.trip_routes import trip_bp
    from routes.booking_routes import booking_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(trip_bp, url_prefix="/trip")
    app.register_blueprint(booking_bp, url_prefix="/booking")
    app.register_blueprint(hotel_bp, url_prefix="/hotel")
    app.register_blueprint(food_bp, url_prefix="/food")
    app.register_blueprint(adventure_bp, url_prefix="/adventure")
    
    app.register_blueprint(matching_bp, url_prefix='/api')
    app.register_blueprint(cost_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')

register_blueprints()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Search Route
@app.route('/search', methods=["GET", "POST"])
def search():
    action = request.args.get("action")  # cost or buddies
    location = request.args.get("location")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if action == "cost":
            # Fetch hotels
            cursor.execute("SELECT name, price, rating FROM hotels WHERE location=%s", (location,))
            hotels_raw = cursor.fetchall()
            hotels = [{"name": row[0], "price": row[1], "rating": row[2]} for row in hotels_raw]

            # Fetch food
            cursor.execute("SELECT name, type, price FROM food WHERE available_in_location=%s", (location,))
            food_raw = cursor.fetchall()
            food = [{"name": row[0], "description": f"{row[1]} - ₹{row[2]}"} for row in food_raw]

            # Fetch adventures
            cursor.execute("SELECT name, type, cost FROM adventures WHERE location=%s", (location,))
            adventures_raw = cursor.fetchall()
            adventures = [{"name": row[0], "description": f"{row[1]} - ₹{row[2]}"} for row in adventures_raw]

            return render_template("cost.html", location=location, hotels=hotels, food=food, adventures=adventures)

        elif action == "buddies":
            cursor.execute("""
                SELECT t.destination, t.start_date, t.end_date, u.name, u.interests
                FROM trips t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.destination = %s AND t.start_date >= %s AND t.end_date <= %s
            """, (location, start_date, end_date))
            
            trips = cursor.fetchall()
            trip_data = [{
                "destination": row[0],
                "start_date": row[1],
                "end_date": row[2],
                "name": row[3],
                "interests": row[4]
            } for row in trips]

            return render_template("search.html", trips=trip_data, location=location, start_date=start_date, end_date=end_date)

        else:
            return "❌ Invalid action specified. Use 'cost' or 'buddies'.", 400

    except Exception as e:
        print("Search Error:", e)
        return "Internal Server Error", 500

    finally:
        cursor.close()

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[0], password):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    return render_template("login.html")


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    interests = request.form.get('interests', '')
    budget = request.form.get('budget', 0)
    password = request.form['password']
    password_hash = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()
        if existing:
            return jsonify({"success": False, "message": "❌ Email already registered!"})
        
        cursor.execute(
            "INSERT INTO users (name, email, phone, interests, budget, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, email, phone, interests, budget, password_hash)
        )
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        print("Signup Error:", e)
        return jsonify({"success": False, "message": "Something went wrong!"})
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(debug=True)
