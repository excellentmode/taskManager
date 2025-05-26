from werkzeug.security import generate_password_hash

from backend import database
from backend.models.user import User

'''
    Создаём тестового юзера в базе данных.
'''


def initialize_data():
    if not User.query.filter_by(username='admin').first():
        hashed = generate_password_hash('admin123')
        user = User(username='admin', password=hashed)

        database.session.add(user)
        database.session.commit()