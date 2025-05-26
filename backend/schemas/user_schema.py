from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserLoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=Length(min=1),
        error_messages={"required": "Поле 'username' обязательно для заполнения."}
    )
    password = fields.Str(
        required=True,
        validate=Length(min=1),
        error_messages={"required": "Поле 'password' обязательно для заполнения."}
    )


class UserRegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=Length(min=1),
        error_messages={"required": "Поле 'username' обязательно для заполнения."}
    )
    password = fields.Str(
        required=True,
        validate=Length(min=1),
        error_messages={"required": "Поле 'password' обязательно для заполнения."}
    )