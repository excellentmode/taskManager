from datetime import datetime

from backend import database


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(512), nullable=False)
    description = database.Column(database.Text, nullable=True)
    is_completed = database.Column(database.Boolean, default=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)