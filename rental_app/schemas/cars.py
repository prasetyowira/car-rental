from marshmallow import Schema, ValidationError, fields, validates
from rental_app.models.cars import Car


class CarSchema(Schema):
    registration_number = fields.String(required=True)
    color = fields.String(required=True)
    today_status = fields.String()

    @validates("registration_number")
    def validate_registration_number(self, value):
        is_valid = Car.query.filter(Car.registration_number == value).first() is None
        if not is_valid:
            raise ValidationError(f"Car with number {value} already exists")

    class Meta:
        ordered = True
