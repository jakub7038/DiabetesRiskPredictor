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

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Use timezone-aware datetime
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    data = db.relationship('UserData', backref='user', uselist=False, cascade="all, delete-orphan")

    logs = db.relationship('Log', backref='user', lazy=True, cascade="all, delete-orphan")

    history = db.relationship('History', backref='user', lazy=True, cascade="all, delete-orphan")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
      
    def __repr__(self):
        return f'<User {self.email}>'

class UserData(db.Model):
    __tablename__ = 'user_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Demographics
    sex = db.Column(db.Boolean, nullable=False) # 0=Female, 1=Male
    age = db.Column(db.Integer, nullable=False) 

    # Health History
    high_bp = db.Column(db.Boolean, default=False, nullable=False)
    high_chol = db.Column(db.Boolean, default=False, nullable=False)
    chol_check = db.Column(db.Boolean, default=False, nullable=False)
    smoker = db.Column(db.Boolean, default=False, nullable=False)
    stroke = db.Column(db.Boolean, default=False, nullable=False)
    heart_disease = db.Column(db.Boolean, default=False, nullable=False)
    
    # Access & Disability
    any_healthcare = db.Column(db.Boolean, default=True, nullable=False)
    no_docbc_cost = db.Column(db.Boolean, default=False, nullable=False)
    diff_walk = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<UserData for User {self.user_id}>'

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)
    
    # Daily Tracking
    ate_fruit = db.Column(db.Boolean, default=False)
    ate_veggie = db.Column(db.Boolean, default=False)
    physical_activity = db.Column(db.Boolean, default=False)
    alcohol_drinks = db.Column(db.Integer, default=0)
    bad_mental_day = db.Column(db.Boolean, default=False)
    bad_physical_day = db.Column(db.Boolean, default=False)
    
    # Biometrics
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

    llm_feedback = db.Column(db.Text, nullable=True)

    input_snapshot = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<History Result {self.result} User {self.user_id}>'