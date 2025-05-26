from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from backend.schemas.task_schema import TaskSchema
from backend.services.task_service import (
    handle_get_tasks,
    handle_add_task,
    handle_update_task,
    handle_delete_task
)

task_bp = Blueprint('tasks', __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    return handle_get_tasks(user_id)


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    try:
        validated_data = task_schema.load(request.get_json())
        return handle_add_task(user_id, validated_data)
    except ValidationError as err:
        return jsonify({'msg': 'Validation error', 'errors': err.messages}), 422


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_existing_task(task_id):
    user_id = get_jwt_identity()
    try:
        # partial=True позволяет обновлять только часть полей
        validated_data = task_schema.load(request.get_json(), partial=True)
        return handle_update_task(task_id, user_id, validated_data)
    except ValidationError as err:
        return jsonify({'msg': 'Validation error', 'errors': err.messages}), 422


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_existing_task(task_id):
    user_id = get_jwt_identity()
    return handle_delete_task(task_id, user_id)