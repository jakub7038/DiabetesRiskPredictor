from flask import Blueprint, request, jsonify
from auth import register_user, login_user

auth_bp = Blueprint('auth', __name__)

# --- REGISTRATION ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    success, message = register_user(data.get('email'), data.get('password'))

    if success:
        return jsonify({"msg": message}), 201
    else:
        return jsonify({"msg": message}), 400

# --- LOGIN ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    result = login_user(data.get('email'), data.get('password'))

    if result:
        return jsonify({
            "msg": "Login successful",
            "data": result
        }), 200
    
    return jsonify({"msg": "Bad email or password"}), 401