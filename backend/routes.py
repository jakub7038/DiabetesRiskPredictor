from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import json
from datetime import datetime, timezone

from models import db, UserData, Log, History, User
from auth import register_user, login_user
from ml_service import predict_diabetes_risk, analyze_risk_trend

# ==========================================
#  AUTH BLUEPRINT (Register, Login, Predict)
# ==========================================
auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200

# --- ML PREDICTION ROUTE ---
@auth_bp.route('/predict', methods=['POST'])
@jwt_required(optional=True)
def predict():
    user_id = get_jwt_identity()
    data = request.get_json()

    predictions, error = predict_diabetes_risk(data)

    if predictions is None:
        return jsonify({"msg": "Prediction failed", "error": error}), 500

    if user_id:
        try:
            # Zapisujemy wszystkie 3 predykcje jako osobne rekordy
            for model_name, pred_data in predictions.items():
                if pred_data is not None:
                    new_history = History(
                        user_id=user_id,
                        result=pred_data['prediction'],
                        probability=pred_data['confidence'],
                        input_snapshot=json.dumps({
                            'input_data': data,
                            'model': model_name,
                            'all_probabilities': pred_data['probabilities']
                        })
                    )
                    db.session.add(new_history)

            db.session.commit()
            print(f"✅ Saved predictions for user {user_id}")

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Prediction done but database save failed", "error": str(e)}), 500

    return jsonify({
        "msg": "Prediction successful",
        "predictions": predictions,
        "is_saved": bool(user_id)
    }), 200


# ==========================================
#  API BLUEPRINT (Logs, User Data)
# ==========================================
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

    # Check if log exists for this day
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

@api_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    user_id = get_jwt_identity()

    # Pobieramy całą historię predykcji tego użytkownika
    user_history = History.query.filter_by(user_id=user_id).all()

    if not user_history:
        return jsonify({"msg": "No history found"}), 404

    # Analiza trendu
    trend_data = analyze_risk_trend(user_history)

    if trend_data is None:
        return jsonify({
            "msg": "Not enough data points for regression (need at least 2)",
            "data": []
        }), 200 # Zwracamy 200, bo to nie błąd serwera, po prostu brak danych do trendu

    return jsonify({
        "msg": "Trend analysis successful",
        "data": trend_data
    }), 200