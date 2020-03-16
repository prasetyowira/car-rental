from sqlalchemy import or_
from marshmallow import ValidationError


class RentsController:
    @staticmethod
    def create(data: dict):
        from rental_app.models.cars import Car as CarModel
        from rental_app.models.logs import Log

        car = CarModel.query.filter(
            CarModel.registration_number == data.get("registration_number"),
        ).first()
        if car is None:
            print("Car Not Found")
            return

        rented_list = Log.query.filter(
            Log.car_id == car.id,
            Log.has_settled.is_(False),
            Log.rent_date == data.get("rent_date")
        ).first()

        if rented_list:
            print("Car Already Rented")
            return

        payload_data = dict(
            car_id=car.id,
            rent_date=data.get("rent_date"),
            customer_name=data.get("customer_name"),
        )

        try:
            log = Log(**payload_data).save()
        except Exception as e:
            return "Internal Server error"
        return f"Reserved {car.registration_number} to {log.customer_name} on {log.rent_date}"

    @staticmethod
    def get(*args, **kwargs):
        from rental_app.models.cars import Car as CarModel
        from rental_app.models.logs import Log

        date = kwargs.get("date", None)

        cars = CarModel.query.outerjoin(Log).all()

        print("Registration No  Color   Status  Customer\n")
        for car in cars:
            status = car.status(date)
            customer = car.get_customer(date)
            print(f"{car.registration_number}   {car.color}     {status.value}      {customer}\n")
