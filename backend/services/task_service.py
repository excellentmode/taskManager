from flask import jsonify

from backend import database
from backend.models.task import Task
from backend.schemas.task_schema import TaskSchema

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


def get_tasks_by_user(user_id):
    return Task.query.filter_by(user_id=user_id).all()


def create_task(title, description, user_id):
    task = Task(title=title, description=description, user_id=user_id)
    database.session.add(task)
    database.session.commit()
    return task


def update_task(task, data):
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'is_completed' in data:
        task.is_completed = data['is_completed']
    database.session.commit()
    return task


def delete_task(task):
    database.session.delete(task)
    database.session.commit()


# === HANDLERS ===
def handle_get_tasks(user_id):
    tasks = get_tasks_by_user(user_id)
    return jsonify(tasks_schema.dump(tasks)), 200


def handle_add_task(user_id, data):
    validated = task_schema.load(data)
    task = create_task(validated['title'], validated.get('description'), user_id)
    return jsonify(task_schema.dump(task)), 201


def handle_update_task(task_id, user_id, data):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'msg': 'Task not found'}), 404
    validated = task_schema.load(data, partial=True)
    task = update_task(task, validated)
    return jsonify(task_schema.dump(task)), 200


def handle_delete_task(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'msg': 'Task not found'}), 404
    delete_task(task)
    return jsonify({'msg': 'Task deleted'}), 200