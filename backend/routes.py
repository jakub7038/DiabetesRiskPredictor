from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import json
from datetime import datetime, timezone

from models import db, UserData, Log, History, User
from auth import register_user, login_user
from ml_service import predict_diabetes_risk, analyze_risk_trend

from services.ai_service import get_ai_response

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

    # === WALIDACJA DANYCH ===
    errors = []

    # Wymagane pola
    if 'Sex' not in data:
        errors.append("Pole 'Sex' jest wymagane")
    elif data['Sex'] not in [0, 1]:
        errors.append("Sex musi być 0 (kobieta) lub 1 (mężczyzna)")

    if 'Age' not in data:
        errors.append("Pole 'Age' jest wymagane")
    elif not (1 <= data['Age'] <= 13):
        errors.append("Age musi być w zakresie 1-13")

    if 'BMI' not in data:
        errors.append("Pole 'BMI' jest wymagane")
    elif not (10 <= data['BMI'] <= 70):
        errors.append("BMI musi być w zakresie 10-70")

    # Walidacja pól opcjonalnych
    if 'GenHlth' in data and not (1 <= data['GenHlth'] <= 5):
        errors.append("GenHlth musi być w zakresie 1-5")

    if 'MentHlth' in data and not (0 <= data['MentHlth'] <= 30):
        errors.append("MentHlth musi być w zakresie 0-30 dni")

    if 'PhysHlth' in data and not (0 <= data['PhysHlth'] <= 30):
        errors.append("PhysHlth musi być w zakresie 0-30 dni")

    # Walidacja pól binarnych
    binary_fields = [
        'HighBP', 'HighChol', 'Smoker', 'Stroke', 'HeartDiseaseorAttack',
        'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'DiffWalk'
    ]

    for field in binary_fields:
        if field in data and data[field] not in [0, 1]:
            errors.append(f"{field} musi być 0 lub 1")

    # Jeśli są błędy walidacji, zwróć 400
    if errors:
        return jsonify({
            "msg": "Błąd walidacji danych",
            "errors": errors
        }), 400

    # === KONIEC WALIDACJI ===

    predictions, error = predict_diabetes_risk(data, is_authenticated=bool(user_id))

    if predictions is None:
        return jsonify({"msg": "Prediction failed", "error": error}), 500

    if user_id:
        try:
            llm_text = predictions.pop('llm_analysis', None)
            shap_list = predictions.pop('shap_factors', [])

            # Extract primary model (Random Forest) data for the main result
            primary_model = predictions.get('random_forest')
            
            # Fallback if Random Forest failed but others didn't (unlikely but safe)
            if not primary_model:
                primary_model = predictions.get('logistic') or predictions.get('gradient_boost')

            if primary_model:
                # Calculate combined risk for the primary model
                probabilities = primary_model.get('probabilities', {})
                diabetes_risk = probabilities.get('class_1', 0) + probabilities.get('class_2', 0)

                # Save ONE history record with all details
                new_history = History(
                    user_id=user_id,
                    result=primary_model['prediction'],
                    probability=diabetes_risk,
                    llm_feedback=llm_text,
                    model_scores=predictions, # Save ALL model predictions here
                    input_snapshot=json.dumps({
                        'input_data': data
                    })
                )
                db.session.add(new_history)
                db.session.commit()

            if llm_text:
                predictions['llm_analysis'] = llm_text

            if shap_list:
                predictions['shap_factors'] = shap_list

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
            "input_data": input_data,
            "model_scores": record.model_scores
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
            "input_snapshot": snapshot_data,
            "model_scores": record.model_scores
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
    


@api_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    """
    Endpoint obsługujący czat. Pobiera dane użytkownika z bazy,
    aby nadać kontekst rozmowie, a następnie pyta Gemini.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # 1. Pobierz kontekst zdrowotny użytkownika (jeśli istnieje)
    user_data = UserData.query.filter_by(user_id=user_id).first()
    context = {}
    
    if user_data:
        # Tłumaczenie danych z bazy na czytelny format dla AI
        context = {
            "sex": "Kobieta" if user_data.sex == 0 else "Mężczyzna",
            "age": f"Kategoria wiekowa {user_data.age}", # Zakładając, że age to kategoria 1-13
            "high_bp": user_data.high_bp,
            "high_chol": user_data.high_chol,
            # Obliczanie BMI jeśli mamy wagę i wzrost w ostatnich logach
            "bmi": None 
        }
        
        # Próba pobrania ostatniej wagi/wzrostu z logów
        last_log = Log.query.filter_by(user_id=user_id).order_by(Log.log_date.desc()).first()
        if last_log and last_log.weight and last_log.height:
            try:
                # height w cm, weight w kg
                height_m = last_log.height / 100
                bmi = last_log.weight / (height_m * height_m)
                context["bmi"] = round(bmi, 2)
            except:
                pass

    # 2. Wywołanie serwisu AI
    ai_response_text = get_ai_response(user_message, user_context=context)

    return jsonify({
        "text": ai_response_text,
        "status": "success"
    }), 200