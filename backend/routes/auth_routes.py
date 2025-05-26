from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import Conflict, BadRequest, Unauthorized

from backend.schemas.user_schema import UserLoginSchema, UserRegisterSchema
from backend.services.user_service import generate_token_from_user
from backend.services.user_service import register_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        validated_data = UserLoginSchema().load(data)
        access_token = generate_token_from_user(**validated_data)
        return jsonify(access_token=access_token), 200
    except ValidationError as ve:
        return jsonify({'msg': 'Ошибка валидации', 'Ошибки': ve.messages}), 422
    except Unauthorized as e:
        return jsonify({'msg': str(e)}), 401
    except Exception as e:
        return jsonify({'msg': str(e)}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        validated_data = UserRegisterSchema().load(data)
        user = register_user(**validated_data)
        return jsonify({'id': user.id, 'username': user.username}), 201
    except ValidationError as ve:
        return jsonify({'msg': 'Ошибка валидации данных', 'ошибки': ve.messages}), 422
    except Conflict as ce:
        return jsonify({'msg': str(ce)}), 409
    except BadRequest as be:
        return jsonify({'msg': str(be)}), 400
    except Exception:
        return jsonify({'msg': 'Внутренняя ошибка сервера'}), 500