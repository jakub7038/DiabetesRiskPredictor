from models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token

def register_user(email, password):

    if not email or not password:
        return False, "Email oraz hasło są wymagane!"

    if User.query.filter_by(email=email).first():
        return False, "Użytkownik juz istnieje!"

    new_user = User(email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return True, "Użytkownik stworzony."
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def login_user(email, password):

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "email": user.email
        }
    
    return None