from marshmallow import fields

from backend import marshmallow_instance


class TaskSchema(marshmallow_instance.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    is_completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)