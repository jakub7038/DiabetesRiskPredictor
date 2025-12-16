from app import app
from models import db, User, Log, History, UserData
from ml_service import predict_diabetes_risk
from datetime import datetime, timedelta, time, timezone
import random
import json

SEED_EMAIL = "useruser@example.com"
SEED_PASSWORD = "password"
DAYS_TO_GENERATE = 45


def clean_existing_user():
    user = User.query.filter_by(email=SEED_EMAIL).first()
    if user:
        db.session.delete(user)
        db.session.commit()


def create_user_and_profile():
    user = User(email=SEED_EMAIL)
    user.set_password(SEED_PASSWORD)
    db.session.add(user)
    db.session.commit()

    user_data = UserData(
        user_id=user.id,
        sex=1,
        age=35,
        high_bp=False,
        high_chol=True,
        chol_check=True,
        smoker=False,
        stroke=False,
        heart_disease=False,
        any_healthcare=True,
        no_docbc_cost=False,
        diff_walk=False
    )
    db.session.add(user_data)
    db.session.commit()

    return user, user_data


def generate_logs_and_history(user, user_data):
    current_date = datetime.now(timezone.utc).date() - timedelta(days=DAYS_TO_GENERATE)

    current_weight = 85.0
    ate_veggie_yesterday = False

    for i in range(DAYS_TO_GENERATE):
        log_date = current_date + timedelta(days=i)

        current_weight += random.uniform(-0.4, 0.3)
        is_weekend = log_date.weekday() >= 5

        alcohol = random.choice([2, 3, 4, 5, 0]) if is_weekend else random.choice([0, 0, 0, 1])

        chance_veggie = 0.8 if ate_veggie_yesterday else 0.3
        ate_veggie = random.random() < chance_veggie
        ate_veggie_yesterday = ate_veggie
        ate_fruit = random.choice([True, False])
        physical_activity = not is_weekend
        bad_mental = random.random() > 0.8
        bad_physical = random.random() > 0.9

        log_entry = Log(
            user_id=user.id,
            log_date=log_date,
            ate_fruit=ate_fruit,
            ate_veggie=ate_veggie,
            physical_activity=physical_activity,
            alcohol_drinks=alcohol,
            bad_mental_day=bad_mental,
            bad_physical_day=bad_physical,
            weight=round(current_weight, 1),
            height=180.0
        )
        db.session.add(log_entry)

        input_data = {
            "sex": 1 if user_data.sex else 0,
            "age": user_data.age,
            "high_bp": 1 if user_data.high_bp else 0,
            "high_chol": 1 if user_data.high_chol else 0,
            "chol_check": 1 if user_data.chol_check else 0,
            "smoker": 1 if user_data.smoker else 0,
            "stroke": 1 if user_data.stroke else 0,
            "heart_disease": 1 if user_data.heart_disease else 0,
            "any_healthcare": 1 if user_data.any_healthcare else 0,
            "no_docbc_cost": 1 if user_data.no_docbc_cost else 0,
            "diff_walk": 1 if user_data.diff_walk else 0,
            "weight": round(current_weight, 1),
            "height": 180.0,
            "ate_fruit": 1 if ate_fruit else 0,
            "ate_veggie": 1 if ate_veggie else 0,
            "physical_activity": 1 if physical_activity else 0,
            "alcohol_drinks": alcohol,
            "bad_mental_day": 1 if bad_mental else 0,
            "bad_physical_day": 1 if bad_physical else 0,
            "gen_hlth": 3
        }

        result, confidence = predict_diabetes_risk(input_data)

        if result is not None:
            fake_timestamp = datetime.combine(log_date, time(12, 0, 0))
            history_entry = History(
                user_id=user.id,
                result=result,
                probability=confidence,
                input_snapshot=json.dumps(input_data),
                created_at=fake_timestamp
            )
            db.session.add(history_entry)

    db.session.commit()


def seed_database():
    with app.app_context():
        clean_existing_user()
        user, user_data = create_user_and_profile()
        generate_logs_and_history(user, user_data)
        print(f"zaseedowało się")


if __name__ == "__main__":
    seed_database()