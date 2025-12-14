from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# --- THIS WAS MISSING ---
# This initializes the database object that app.py is trying to import
db = SQLAlchemy()
# ------------------------

# 1. USERS TABLE
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # uselist=False makes this a 1-to-1 relationship
    user_data = db.relationship('UserData', backref='user', uselist=False) 
    # lazy=True means logs aren't loaded until you ask for them
    logs = db.relationship('Log', backref='user', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)

    # Security Methods (Used by auth.py)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 2. USER DATA TABLE (Static Health Profile)
class UserData(db.Model):
    __tablename__ = 'user_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    sex = db.Column(db.Boolean)
    age = db.Column(db.Integer)
    high_bp = db.Column(db.Boolean)
    high_chol = db.Column(db.Boolean)
    chol_check = db.Column(db.Boolean)
    smoker = db.Column(db.Boolean)
    stroke = db.Column(db.Boolean)
    heart_disease = db.Column(db.Boolean)
    any_healthcare = db.Column(db.Boolean)
    no_docbc_cost = db.Column(db.Boolean)
    diff_walk = db.Column(db.Boolean)

# 3. LOGS TABLE (Daily Entries)
class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.Date, default=datetime.utcnow)
    
    ate_fruit = db.Column(db.Boolean)
    ate_veggie = db.Column(db.Boolean)
    physical_activity = db.Column(db.Boolean)
    alcohol_drinks = db.Column(db.Integer)
    bad_mental_day = db.Column(db.Boolean)
    bad_physical_day = db.Column(db.Boolean)
    weight = db.Column(db.Numeric(5, 2))
    height = db.Column(db.Numeric(5, 2))

# 4. HISTORY TABLE (ML Predictions)
class History(db.Model):
    __tablename__ = 'history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    result = db.Column(db.Integer)       # 0 or 1
    probability = db.Column(db.Float)    # e.g., 0.85
    input_snapshot = db.Column(db.JSON)  # Stores the exact data used for prediction

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