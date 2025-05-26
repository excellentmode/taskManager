from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
jwt_instance = JWTManager()
marshmallow_instance = Marshmallow()


def create_app(test_config=None):
    app = Flask(__name__)

    # конфиг для бд
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/db_task_manager'
    app.config['JWT_SECRET_KEY'] = 'very-super-secret-key-test-123'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # перезапись конфига для тестов
    if test_config:
        app.config.update(test_config)

    CORS(app)
    database.init_app(app)
    jwt_instance.init_app(app)
    marshmallow_instance.init_app(app)

    from backend.routes.auth_routes import auth_bp
    from backend.routes.task_routes import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    with app.app_context():
        try:
            from backend.migrations.init_data import initialize_data
            database.create_all()
            initialize_data()
        except Exception as e:
            print("Ошибка при подключении к базе данных:", e)

    return app