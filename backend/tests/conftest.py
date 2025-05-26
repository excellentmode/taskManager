import pytest
from werkzeug.security import generate_password_hash

from backend import create_app, database
from backend.models.user import User


@pytest.fixture
def client():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key'
    }

    app = create_app(test_config=test_config)

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        return {'msg': 'Validation error', 'errors': err.exc.messages}, 422

    @app.errorhandler(400)
    def handle_bad_request(err):
        return {'msg': str(err)}, 400

    @app.errorhandler(500)
    def handle_internal_error(err):
        return {'msg': 'Internal server error'}, 500

    with app.app_context():
        database.create_all()
        if not User.query.filter_by(username='admin').first():
            hashed = generate_password_hash('admin123')
            user = User(username='admin', password=hashed)
            database.session.add(user)
            database.session.commit()

    yield app.test_client()