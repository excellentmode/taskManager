from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from backend import database
from backend.models.user import User


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if not user or not check_password_hash(user.password, password):
        raise Unauthorized("Invalid credentials")
    return user


def generate_token_from_user(username, password):
    user = authenticate_user(username, password)
    return create_access_token(identity=str(user.id))


def register_user(username: str, password: str) -> User:
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise Conflict("Пользователь с таким именем уже существует.")

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    database.session.add(new_user)
    database.session.commit()
    return new_user