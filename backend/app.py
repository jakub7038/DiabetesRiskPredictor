from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_predictor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    pass


class UserData(db.Model):
    pass


class Log(db.Model):
    pass


class History(db.Model):
    pass


@app.route('/register', methods=['POST'])
def register():
    pass


@app.route('/update_profile/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    pass


@app.route('/add_log/<int:user_id>', methods=['POST'])
def add_log(user_id):
    pass


@app.route('/predict/<int:user_id>', methods=['POST'])
def predict_health(user_id):
    pass


def get_age_category(age):
    return int(max(1, min(13, (age - 15) // 5)))


@app.route('/predict_full/<int:user_id>', methods=['POST'])
def predict_full(user_id):
    data = request.get_json()

    weight = data.get('Weight', 0)
    height = data.get('Height', 1)
    bmi = round(weight / (height ** 2), 2)

    age_category = get_age_category(data.get('Age', 30))

    sex = data.get('Sex', 0)
    drinks_per_week = data.get('AlcoholDrinksPerWeek', 0)

    hvy_alcohol = 0
    if (sex == 1 and drinks_per_week > 14) or (sex == 0 and drinks_per_week > 7):
        hvy_alcohol = 1

    input_vector = [
        data.get('HighBP', 0),
        data.get('HighChol', 0),
        data.get('CholCheck', 0),
        bmi,
        data.get('Smoker', 0),
        data.get('Stroke', 0),
        data.get('Diabetes_012', 0),
        data.get('PhysActivity', 0),
        data.get('Fruits', 0),
        data.get('Veggies', 0),
        hvy_alcohol,
        data.get('AnyHealthcare', 0),
        data.get('NoDocbcCost', 0),
        data.get('GenHlth', 3),
        data.get('MentHlth', 0),
        data.get('PhysHlth', 0),
        data.get('DiffWalk', 0),
        sex,
        age_category
    ]

    # prediction = model.predict([input_vector])
    # probability = model.predict_proba([input_vector])

    # --- usuwanko --- gdy powstanie model
    risk_score = 0.0
    if bmi > 30: risk_score += 0.3
    if data.get('HighBP'): risk_score += 0.25
    if data.get('Diabetes_012') == 2: risk_score += 0.3
    if data.get('Smoker'): risk_score += 0.15
    if age_category > 9: risk_score += 0.2


    probability = min(risk_score, 0.99)
    result = 1 if probability > 0.5 else 0
    # --- usuwanko ---


    new_history = History(
        user_id=user_id,
        result=result,
        probability=round(probability, 4),
        input_snapshot={
            'input_vector': input_vector,
            'calculated_bmi': bmi,
            'calculated_age_cat': age_category,
            'raw_data': data
        }
    )

    try:
        db.session.add(new_history)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'prediction': result,
        'probability': probability,
        'details': {
            'bmi': bmi,
            'age_category': age_category,
            'heavy_drinker': hvy_alcohol
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Baza danych gotowa.")

    app.run(debug=True) # usuwamy na koniec