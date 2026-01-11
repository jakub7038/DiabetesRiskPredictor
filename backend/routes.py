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
# ZAMIEŃ TĘ CZĘŚĆ W routes.py w endpoincie /predict

@auth_bp.route('/predict', methods=['POST'])
@jwt_required(optional=True)
def predict():
    user_id = get_jwt_identity()
    data = request.get_json()

    predictions, error = predict_diabetes_risk(data, is_authenticated=bool(user_id))

    if predictions is None:
        return jsonify({"msg": "Prediction failed", "error": error}), 500

    if user_id:
        try:
            llm_text = predictions.pop('llm_analysis', None)
            shap_list = predictions.pop('shap_factors', [])

            for model_name, pred_data in predictions.items():
                if pred_data is not None:
                    # POPRAWKA: Oblicz prawdziwe ryzyko cukrzycy (klasa 1 + klasa 2)
                    probabilities = pred_data.get('probabilities', {})
                    diabetes_risk = probabilities.get('class_1', 0) + probabilities.get('class_2', 0)

                    new_history = History(
                        user_id=user_id,
                        result=pred_data['prediction'],
                        probability=diabetes_risk,  # <- TUTAJ ZMIENIAMY z confidence na diabetes_risk
                        llm_feedback=llm_text if model_name == 'random_forest' else None,
                        input_snapshot=json.dumps({
                            'input_data': data,
                            'model': model_name,
                            'all_probabilities': pred_data['probabilities']
                        })
                    )
                    db.session.add(new_history)

            db.session.commit()

            if llm_text:
                predictions['llm_analysis'] = llm_text

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


@api_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Pobiera historię predykcji użytkownika"""
    user_id = get_jwt_identity()

    # Opcjonalny parametr limit
    limit = request.args.get('limit', type=int)

    query = History.query.filter_by(user_id=user_id).order_by(History.created_at.desc())

    if limit:
        query = query.limit(limit)

    history_records = query.all()

    result = []
    for record in history_records:
        # Parsowanie input_snapshot
        input_data = {}
        if record.input_snapshot:
            try:
                snapshot = json.loads(record.input_snapshot)
                input_data = snapshot.get('input_data', {})
            except:
                pass

        # Helper function do etykiet
        result_labels = {
            0: "Brak cukrzycy",
            1: "Stan przedcukrzycowy",
            2: "Cukrzyca"
        }

        result.append({
            "id": record.id,
            "created_at": record.created_at.isoformat(),
            "result": record.result,
            "result_label": result_labels.get(record.result, "Nieznany"),
            "probability": record.probability,
            "llm_feedback": record.llm_feedback,
            "input_data": input_data
        })

    return jsonify({
        "msg": "History retrieved successfully",
        "count": len(result),
        "data": result
    }), 200


@api_bp.route('/history/<int:history_id>', methods=['GET'])
@jwt_required()
def get_history_detail(history_id):
    """Pobiera szczegóły pojedynczej predykcji"""
    user_id = get_jwt_identity()

    record = History.query.filter_by(id=history_id, user_id=user_id).first()

    if not record:
        return jsonify({"msg": "History record not found"}), 404

    # Parsowanie input_snapshot
    snapshot_data = {}
    if record.input_snapshot:
        try:
            snapshot_data = json.loads(record.input_snapshot)
        except:
            pass

    result_labels = {
        0: "Brak cukrzycy",
        1: "Stan przedcukrzycowy",
        2: "Cukrzyca"
    }

    return jsonify({
        "msg": "History detail retrieved successfully",
        "data": {
            "id": record.id,
            "created_at": record.created_at.isoformat(),
            "result": record.result,
            "result_label": result_labels.get(record.result, "Nieznany"),
            "probability": record.probability,
            "llm_feedback": record.llm_feedback,
            "input_snapshot": snapshot_data
        }
    }), 200


@api_bp.route('/history/<int:history_id>', methods=['DELETE'])
@jwt_required()
def delete_history(history_id):
    """Usuwa pojedynczy rekord historii"""
    user_id = get_jwt_identity()

    record = History.query.filter_by(id=history_id, user_id=user_id).first()

    if not record:
        return jsonify({"msg": "History record not found"}), 404

    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"msg": "History record deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@api_bp.route('/user-data', methods=['GET'])
@jwt_required()
def get_user_data():
    """Pobiera dane użytkownika"""
    user_id = get_jwt_identity()

    user_data = UserData.query.filter_by(user_id=user_id).first()

    if not user_data:
        return jsonify({
            "msg": "No user data found",
            "data": None
        }), 200

    return jsonify({
        "msg": "User data retrieved successfully",
        "data": {
            "sex": user_data.sex,
            "age": user_data.age,
            "high_bp": user_data.high_bp,
            "high_chol": user_data.high_chol,
            "chol_check": user_data.chol_check,
            "smoker": user_data.smoker,
            "stroke": user_data.stroke,
            "heart_disease": user_data.heart_disease,
            "any_healthcare": user_data.any_healthcare,
            "no_docbc_cost": user_data.no_docbc_cost,
            "diff_walk": user_data.diff_walk
        }
    }), 200


@api_bp.route('/user-data', methods=['POST'])
@jwt_required()
def save_user_data():
    """Zapisuje lub aktualizuje dane użytkownika"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Walidacja wymaganych pól
    if 'sex' not in data or 'age' not in data:
        return jsonify({"msg": "Sex and age are required"}), 400

    user_data = UserData.query.filter_by(user_id=user_id).first()

    try:
        if user_data:
            # Aktualizacja istniejących danych
            user_data.sex = data.get('sex')
            user_data.age = data.get('age')
            user_data.high_bp = data.get('high_bp', False)
            user_data.high_chol = data.get('high_chol', False)
            user_data.chol_check = data.get('chol_check', False)
            user_data.smoker = data.get('smoker', False)
            user_data.stroke = data.get('stroke', False)
            user_data.heart_disease = data.get('heart_disease', False)
            user_data.any_healthcare = data.get('any_healthcare', True)
            user_data.no_docbc_cost = data.get('no_docbc_cost', False)
            user_data.diff_walk = data.get('diff_walk', False)
        else:
            # Tworzenie nowych danych
            user_data = UserData(
                user_id=user_id,
                sex=data.get('sex'),
                age=data.get('age'),
                high_bp=data.get('high_bp', False),
                high_chol=data.get('high_chol', False),
                chol_check=data.get('chol_check', False),
                smoker=data.get('smoker', False),
                stroke=data.get('stroke', False),
                heart_disease=data.get('heart_disease', False),
                any_healthcare=data.get('any_healthcare', True),
                no_docbc_cost=data.get('no_docbc_cost', False),
                diff_walk=data.get('diff_walk', False)
            )
            db.session.add(user_data)

        db.session.commit()

        return jsonify({
            "msg": "User data saved successfully",
            "data": {
                "sex": user_data.sex,
                "age": user_data.age
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500