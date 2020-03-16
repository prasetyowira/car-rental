from datetime import datetime
from logging import getLogger

import click
from flask.cli import AppGroup

from rental_app.controllers.cars import CarsController
from rental_app.controllers.rents import RentsController

car_cli = AppGroup("car", help="all cli related to car")
rent_cli = AppGroup("rent", help="all cli related to rent")

_log = getLogger(__name__)


@car_cli.command("create")
@click.argument("registration_number")
@click.argument("color")
def create_car(registration_number: str, color: str):
    if registration_number == "" or color == "":
        raise NotImplementedError
    result = CarsController.create(data=dict(
        registration_number=registration_number,
        color=color
    ))
    print(result)


@car_cli.command("search")
@click.argument("registration_number")
def search_car(registration_number: str):
    result = CarsController.get(keyword=registration_number)
    print(result)


@rent_cli.command("status", context_settings={"ignore_unknown_options": True})
@click.argument("date", nargs=-1)
def daily_status(date: tuple):
    if len(date) == 0:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = date[0]
    result = RentsController.get(date=date)
    print(result)


@rent_cli.command("reserve", context_settings={"ignore_unknown_options": True})
@click.argument("registration_number", nargs=1)
@click.argument("customer_name", nargs=1)
@click.argument("date", nargs=1)
def reserve(registration_number: str, customer_name: str, date: str):
    if registration_number == "" or customer_name == "":
        raise NotImplementedError

    rent_date = datetime.strptime(date, "%Y-%m-%d")
    result = RentsController.create(dict(
        registration_number=registration_number,
        customer_name=customer_name,
        rent_date=rent_date
    ))
    print(result)


@rent_cli.command("rent", context_settings={"ignore_unknown_options": True})
@click.argument("registration_number", nargs=1)
@click.argument("customer_name", nargs=1)
@click.argument("date", nargs=1)
def rent(registration_number: str, customer_name: str, date: str):
    if registration_number == "" or customer_name == "":
        raise NotImplementedError

    rent_date = datetime.strptime(date, "%Y-%m-%d")
    result = RentsController.create(dict(
        registration_number=registration_number,
        customer_name=customer_name,
        rent_date=rent_date
    ))
    print(result)
