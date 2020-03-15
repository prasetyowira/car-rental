from datetime import datetime
from logging import getLogger

import click
from flask import current_app
from flask.cli import AppGroup

car_cli = AppGroup("car", help="all cli related to car")
rent_cli = AppGroup("rent", help="all cli related to rent")

_log = getLogger(__name__)


@car_cli.command("create")
@click.argument("registration_number")
@click.argument("color")
def create_car(registration_number: str, color: str):
    if registration_number == "" or color == "":
        raise NotImplementedError
    print(registration_number)
    print(color)


@car_cli.command("search")
@click.argument("registration_number")
def search_car(registration_number: str):
    print(registration_number)


@rent_cli.command("status", context_settings={"ignore_unknown_options": True})
@click.argument("date", nargs=-1)
def daily_status(date: tuple):
    if len(date) == 0:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = date[0]
    print(date)


@rent_cli.command("reserve", context_settings={"ignore_unknown_options": True})
@click.argument("registration_number", nargs=1)
@click.argument("name", nargs=1)
@click.argument("date", nargs=-1)
def reserve(registration_number: str, name: str, date: tuple):
    if registration_number == "" or name == "":
        raise NotImplementedError

    if len(date) == 0:
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif len(date) == 1:
        start_date = date[0]
        end_date = start_date
    else:
        start_date = date[0]
        end_date = date[1]
    print(date)


@rent_cli.command("rent", context_settings={"ignore_unknown_options": True})
@click.argument("registration_number", nargs=1)
@click.argument("name", nargs=1)
@click.argument("date", nargs=-1)
def rent(registration_number: str, name: str, date: tuple):
    if registration_number == "" or name == "":
        raise NotImplementedError

    if len(date) == 0:
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif len(date) == 1:
        start_date = date[0]
        end_date = start_date
    else:
        start_date = date[0]
        end_date = date[1]
    print(date)
