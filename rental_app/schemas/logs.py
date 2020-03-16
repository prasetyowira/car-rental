from marshmallow import Schema, fields


class LogSchema(Schema):  # pragma: no cover
    car_id = fields.Integer(required=True)
    customer_name = fields.String(required=True)
    rent_date = fields.Date(required=True)
    inquiry_at = fields.DateTime(required=False)
    has_settled = fields.Boolean(required=False)

    class Meta:
        ordered = True
