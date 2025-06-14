from flask import Blueprint, request, jsonify
from config import mysql
import datetime

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/send', methods=['POST'])
def send_message():
    data = request.json
    cursor = mysql.connection.cursor()
    query = "INSERT INTO chats (sender_id, receiver_id, message, sent_at) VALUES (%s, %s, %s, %s)"
    timestamp = datetime.datetime.now()
    cursor.execute(query, (data['sender_id'], data['receiver_id'], data['message'], timestamp))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"success": True, "message": "Message sent"})

@chat_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    cursor = mysql.connection.cursor()
    query = """
        SELECT sender_id, receiver_id, message, sent_at FROM chats
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY sent_at
    """
    cursor.execute(query, (user1, user2, user2, user1))
    messages = cursor.fetchall()
    cursor.close()
    return jsonify([
        {"sender": m[0], "receiver": m[1], "message": m[2], "time": m[3].strftime("%Y-%m-%d %H:%M")} for m in messages
    ])