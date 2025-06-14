from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from db import mysql
from models.user_model import create_user, get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password_hash'])

    return create_user(name, email, password)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = get_user(email)

    if not user or 'password' not in user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if check_password_hash(user['password'], password):
        token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({
            'access_token': token,
            'message': 'Login successful'
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
