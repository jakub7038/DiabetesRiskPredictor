import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///health_predictor.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    """
    podczas uruchamiania apki stwórz plik .env w folderze /backend i wklej to do środka
    
    
    SECRET_KEY=zmiennarandom
    JWT_SECRET_KEY=zmiennarandom
    DATABASE_URL=sqlite:///health_predictor.db
    """