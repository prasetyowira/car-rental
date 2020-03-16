from datetime import datetime as py_datetime, timedelta
from mimesis import Address, Business, Datetime, Internet, Numbers, Person, random, Text

person = Person()
addr = Address()
number = Numbers()
business = Business()
datetime = Datetime()
internet = Internet()
random = random.Random()
text = Text()

date_format = "%Y-%m-%d"


def generate_car_data():
    return dict(
        registration_number=generate_car_registration_code(),
        color=generate_car_color()
    )


def generate_car_registration_code():
    return random.custom_code(mask='@@-####')


def generate_car_color():
    return text.color()


def generate_rent_data(car_id=None):
    data = dict(
        customer_name=generate_customer(),
        date=generate_rent_date(),
    )

    if car_id is not None:
        data.update(car_id=car_id)

    return data


def generate_customer():
    return person.name()


def generate_rent_date():
    return datetime.formatted_date(fmt=date_format, start=2020, end=2020)


def generate_redis_sample_data():
    return "abc"
