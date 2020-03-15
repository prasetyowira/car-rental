from datetime import datetime

from marshmallow import Schema, ValidationError, fields, validates
from marshmallow.validate import OneOf

from rental_app.tools.commons import enum_comprehensions
from rental_app.enums import CarStatusStatus


class CarSchema(Schema):
    registration_number = fields.String(required=True)
    color = fields.String(required=True)
    status = fields.String(
        required=True, validate=OneOf(enum_comprehensions(CarStatusStatus))
    )

    class Meta:
        ordered = True
