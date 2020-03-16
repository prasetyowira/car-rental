from datetime import datetime

from marshmallow import Schema, ValidationError, fields, validates


class LogSchema(Schema):
    car_id = fields.Integer(required=True)
    customer_name = fields.String(required=True)
    rent_date = fields.Date(required=True)
    inquiry_at = fields.DateTime(required=False)
    has_settled = fields.Boolean(required=False)

    class Meta:
        ordered = True
