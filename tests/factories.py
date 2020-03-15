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


def generate_customer():
    return person.name()


def generate_start_rent():
    return datetime.formatted_date(fm=date_format, min=2020, end=2020)


def generate_end_rent(start_date: str):
    start = py_datetime.strptime(start_date, date_format)
    end = start - timedelta(days=365)
    while start > end:
        end_date = datetime.formatted_date(fm=date_format, end=2021)
        end = py_datetime.strptime(end_date, date_format)
    return end_date


def generate_redis_sample_data():
    return "abc"
