from sqlalchemy import or_
from marshmallow import ValidationError


class RentsController:
    @staticmethod
    def create(data: dict):
        from rental_app.schemas.logs import LogSchema
        from rental_app.models.cars import Car
        from rental_app.models.logs import Log

        car = Car.query.filter_by(
            Car.registration_number=data.get("registration_number"),
            Car.status = CarStatusStatus.FREE
        ).first()
        if car is None:
            print("Car Not Found")
            return

        rented_list = Log.query.filter(
            Log.car_id==car.id,
            Log.has_settled.is_(False),
            Log.rent_date==data.get("rent_date")
        ).first()

        if rented_list:
            print("Car Already Rented")
            return

        payload_data = dict(
            car_id=car.id,
            rent_date=data.get("rent_date"),
            customer_name=data.get("customer_name")
        )

        schema = LogSchema()
        try:
            schema_data = schema.load(payload_data)
        except ValidationError as e:
            return f"Validation Error {e}"

        try:
            log = Log(**schema_data).save()
        except Exception as e:
            return "Internal Server error"
        return f"Reserved {log.registration_number} to {log.customer_name} on {log.rent_date}"

    @staticmethod
    def get(*args, **kwargs) -> str:
        from rental_app.models.cars import Car
        keyword = kwargs.get("keyword")
        cars = Car.query.filter(
            or_(
                Car.registration_number == keyword,
                Car.color.ilike(f"%{keyword}%")
            )
        ).all()

        print("|    Registration No     |   Color   |\n")
        for car in cars:
            print(f"|    {car.registration_number}     |   {car.color}   |\n")
