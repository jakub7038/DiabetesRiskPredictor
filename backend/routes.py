from flask import Blueprint, request, jsonify
<<<<<<< HEAD
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import db, UserData, Log, History, User
from auth import register_user, login_user
from datetime import datetime, timezone
=======
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from auth import register_user, login_user
from ml_service import predict_diabetes_risk
from models import db, History
>>>>>>> a9e0b9e (Finished backend ML logic)

auth_bp = Blueprint('auth', __name__)

#  Auth Route

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, message = register_user(data.get('email'), data.get('password'))

    if success:
        return jsonify({"msg": message}), 201
    else:
        return jsonify({"msg": message}), 400

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

<<<<<<< HEAD

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)

    return jsonify({"access_token": new_access_token}), 200


api_bp = Blueprint('api', __name__)


@api_bp.route('/logs', methods=['POST'])
@jwt_required()
def add_log():
    current_user_id = get_jwt_identity()

    data = request.get_json()

    try:
        if 'date' in data:
            log_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        else:
            log_date = datetime.now(timezone.utc).date()
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    existing_log = Log.query.filter_by(user_id=current_user_id, log_date=log_date).first()
    if existing_log:
        return jsonify({"msg": "Log for this date already exists"}), 409

    new_log = Log(
        user_id=current_user_id,
        log_date=log_date,
        ate_fruit=data.get('ate_fruit', False),
        ate_veggie=data.get('ate_veggie', False),
        physical_activity=data.get('physical_activity', False),
        alcohol_drinks=data.get('alcohol_drinks', 0),
        bad_mental_day=data.get('bad_mental_day', False),
        bad_physical_day=data.get('bad_physical_day', False),
        weight=data.get('weight'),
        height=data.get('height')
    )

    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"msg": "Log added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@api_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    current_user_id = get_jwt_identity()

    user_logs = Log.query.filter_by(user_id=current_user_id).order_by(Log.log_date.desc()).all()

    result = []
    for log in user_logs:
        result.append({
            "id": log.id,
            "date": log.log_date.strftime('%Y-%m-%d'),
            "ate_fruit": log.ate_fruit,
            "ate_veggie": log.ate_veggie,
            "physical_activity": log.physical_activity,
            "alcohol_drinks": log.alcohol_drinks,
            "bad_mental_day": log.bad_mental_day,
            "bad_physical_day": log.bad_physical_day,
            "weight": log.weight,
            "height": log.height
        })

    return jsonify(result), 200
=======
 # ML Route

@auth_bp.route('/predict', methods=['POST'])
@jwt_required() # Uzytkownik musi byc zalogowany
def predict():

    user_id = get_jwt_identity()
    
    data = request.get_json()

    result, confidence = predict_diabetes_risk(data)

    if result is None:
        return jsonify({"msg": "Prediction failed", "error": confidence}), 500

    try:
        new_history = History(
            user_id=user_id,
            result=result,
            probability=confidence,
            input_snapshot=json.dumps(data) 
        )
        db.session.add(new_history)
        db.session.commit()

        return jsonify({
            "msg": "Prediction successful",
            "result": result,       
            "probability": confidence
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500
>>>>>>> a9e0b9e (Finished backend ML logic)
