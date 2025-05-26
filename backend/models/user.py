from backend import database


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(512), unique=True, nullable=False)
    password = database.Column(database.String(512), nullable=False)