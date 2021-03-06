from rental_app import create_app, db
from behave import fixture


@fixture
def flask_app(context):
    context.app = create_app(test=True)
    yield context.app


@fixture
def flask_db(context):
    context.db = db
    context.db.app = context.app
    yield context.db


@fixture
def cli_runner(context):
    context.cli_runner = context.app.test_cli_runner()
    yield context.cli_runner


@fixture
def flask_client(context):
    context.client = context.app.test_client()
    yield context.client
