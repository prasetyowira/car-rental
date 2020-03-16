class RentsController:
    @staticmethod
    def create(data: dict) -> str:
        from rental_app.models.cars import Car as CarModel
        from rental_app.models.logs import Log
        car = CarModel.query.filter(
            CarModel.registration_number == data.get("registration_number"),
        ).first()

        if car is None:
            return "Car Not Found"

        rented_list = Log.query.filter(
            Log.car_id == car.id,
            Log.has_settled.is_(False),
            Log.rent_date == data.get("rent_date")
        ).first()

        if rented_list:
            return "Car Already Rented"

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
    def get(*args, **kwargs) -> str:
        from rental_app.models.cars import Car as CarModel
        from rental_app.models.logs import Log

        date = kwargs.get("date", None)

        cars = CarModel.query.outerjoin(Log).all()

        title = f"{'Registration No':<30}{'Color':<10}{'Status':<10}{'Customer':>10}\n"
        content = ""
        for car in cars:
            status = car.status(date)
            customer = car.get_customer(date)
            content += f"{car.registration_number:<30}{car.color:<10}{status.value:<10}{customer:>10}\n"

        return title + content
