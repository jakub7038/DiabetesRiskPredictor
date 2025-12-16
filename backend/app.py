from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
<<<<<<< HEAD
from routes import auth_bp, api_bp
=======
from routes import auth_bp
from ml_service import load_model
>>>>>>> a9e0b9e (Finished backend ML logic)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True, port=5000)

=======
    with app.app_context():
        db.create_all()
        load_model() 
    app.run(debug=True, port=5000)
>>>>>>> a9e0b9e (Finished backend ML logic)
