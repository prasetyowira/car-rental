from marshmallow import ValidationError


class CarsController:
    @staticmethod
    def create(data: dict) -> str:
        from rental_app.schemas.cars import CarSchema
        from rental_app.models.cars import Car
        schema = CarSchema()
        try:
            schema_data = schema.load(data)
        except ValidationError as e:
            return f"Validation Error {e}"

        try:
            car = Car(**schema_data).save()
        except Exception as e:
            return "Internal Server error"
        return f"Car {car.registration_number} {car.color} saved"
