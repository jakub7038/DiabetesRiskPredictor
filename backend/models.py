"""

USERS
id	INTEGER/SERIAL PK
email VARCHAR(255)
password_hash VARCHAR(255)
created_at TIMESTAMP

USER DATA
id	INTEGER/SERIAL PK
user_id	FK - users (1:1)
Sex	Bool
Age	Int
HighBP Bool
HighChol Bool
CholCheck Bool
Smoker Bool
Stroke Bool
HeartDisease Bool
AnyHealthcare Bool
NoDocbcCost	Bool
DiffWalk Bool


LOGS (te dane sie licza dzisiejszego dnia)
id	INTEGER/SERIAL PK
user_id	FK - users (N:1)
log_date Date
ate_fruit Bool
ate_veggie Bool
physical_activity Bool
alcohol_drinks Int
bad_mental_day Bool
bad_physical_day Bool
weight Decimal
height Decimal

HISTORY
id INTEGER/SERIAL PK
user_id FK - users (N:1)
created_at TIMESTAMP
result INTEGER
probability FLOAT
input_snapshot JSON


"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime, timezone


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_predictor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacja user 1:1 UserData
    data = db.relationship('UserData', backref='user', uselist=False, cascade="all, delete-orphan")
    # Relacja user 1:N Logs
    logs = db.relationship('Log', backref='user', lazy=True)
    # Relacja user 1:N History
    history = db.relationship('History', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class UserData(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    sex = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    high_bp = db.Column(db.Boolean, default=False)
    high_chol = db.Column(db.Boolean, default=False)
    chol_check = db.Column(db.Boolean, default=False)
    smoker = db.Column(db.Boolean, default=False)
    stroke = db.Column(db.Boolean, default=False)
    heart_disease = db.Column(db.Boolean, default=False)
    any_healthcare = db.Column(db.Boolean, default=True)
    no_docbc_cost = db.Column(db.Boolean, default=False)
    diff_walk = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<UserData for User {self.user_id}>'


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)

    ate_fruit = db.Column(db.Boolean, default=False)
    ate_veggie = db.Column(db.Boolean, default=False)
    physical_activity = db.Column(db.Boolean, default=False)
    alcohol_drinks = db.Column(db.Integer, default=0)
    bad_mental_day = db.Column(db.Boolean, default=False)
    bad_physical_day = db.Column(db.Boolean, default=False)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)

    def __repr__(self):
        return f'<Log {self.log_date} User {self.user_id}>'


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    result = db.Column(db.Integer, nullable=False)
    probability = db.Column(db.Float, nullable=False)

    input_snapshot = db.Column(JSON, nullable=True)

    def __repr__(self):
        return f'<History Result {self.result} User {self.user_id}>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Baza danych została utworzona pomyślnie: health_predictor.db")

