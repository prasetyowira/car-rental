from rental_app import db
from behave import use_fixture
from tests.behave.features.fixtures import (
    flask_app,
    flask_client,
    flask_db,
)


def before_all(context):
    use_fixture(flask_app, context)
    use_fixture(flask_db, context)
    use_fixture(flask_client, context)
    context.db.create_all()
    clean_db(context.db)


def clean_db(database):
    for table in reversed(db.metadata.sorted_tables):
        database.session.execute(table.delete())
        database.session.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1")


def after_all(context):
    context.db.session.rollback()
    context.db.drop_all()
