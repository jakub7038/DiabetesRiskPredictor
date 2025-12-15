from app import app
from models import db, User, Log
from datetime import datetime, timedelta, timezone
import random

def seed_database():
    with app.app_context():

        email = "useruser@example.com"
        password = "password"

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Utworzono użytkownika: {email}")

        current_date = datetime.now(timezone.utc).date() - timedelta(days=45)
        current_weight = 85.0
        ate_veggie_yesterday = False
        logs_created = 0

        for i in range(45):
            log_date = current_date + timedelta(days=i)

            if Log.query.filter_by(user_id=user.id, log_date=log_date).first():
                continue

            current_weight += random.uniform(-0.4, 0.3)

            is_weekend = log_date.weekday() >= 5
            alcohol = random.choice([2, 3, 4, 5, 0]) if is_weekend else random.choice([0, 0, 0, 1])

            chance = 0.8 if ate_veggie_yesterday else 0.3
            ate_veggie = random.random() < chance
            ate_veggie_yesterday = ate_veggie

            log = Log(
                user_id=user.id,
                log_date=log_date,
                ate_fruit=random.choice([True, False]),
                ate_veggie=ate_veggie,
                physical_activity=not is_weekend,
                alcohol_drinks=alcohol,
                bad_mental_day=random.random() > 0.8,
                bad_physical_day=random.random() > 0.9,
                weight=round(current_weight, 1),
                height=180.0
            )

            db.session.add(log)
            logs_created += 1

        db.session.commit()
        print(f"Zakończono seedowanie. Dodano {logs_created} nowych logów.")


if __name__ == "__main__":
    seed_database()