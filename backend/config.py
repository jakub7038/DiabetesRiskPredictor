import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()

class Config:
    # Now we get the value from the environment, not hardcoded text
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')