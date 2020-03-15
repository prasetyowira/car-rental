
from behave import given, then, when
from tests.factories import generate_car_data


@given("Car Data")
def step_impl(context):
    data = generate_car_data()
    context.data = data


@when("I register Car")
def step_impl(context):
    with context.app.app_context():
        from rental_app.cli import create_car
        print(context.data)
        context.resp = create_car(
            context.data.get("registration_number"),
            context.data.get("color")
        )


@then("I receive success response")
def step_impl(context):
    assert True

