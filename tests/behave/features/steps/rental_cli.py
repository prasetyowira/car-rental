
from behave import given, then, when
from tests.factories import generate_car_data, generate_rent_data


@given("Car Data")
def step_impl(context):
    data = generate_car_data()
    context.data = data


@given("Rent Data")
def step_impl(context):
    rent_data = generate_rent_data(getattr(context, "car_id", None))
    context.rent_data = rent_data


@given("Rent Data on {date}")
def step_impl(context, date):
    rent_data = generate_rent_data(getattr(context, "car_id", None))
    rent_data.update(date=date)
    context.rent_data = rent_data


@given("Car success Saved")
def step_impl(context):
    from rental_app.models.cars import Car
    saved = Car(
        registration_number=context.data.get("registration_number"),
        color=context.data.get("color")
    ).save()
    context.saved = saved
    context.car_id = saved.id


@when("I register Car")
def step_impl(context):
    with context.app.app_context():
        from rental_app.cli import create_car
        cli_runner = context.cli_runner
        context.resp = cli_runner.invoke(
            create_car,
            [context.data.get("registration_number"), context.data.get("color")]
        )


@when("I search Car by registration number")
def step_impl(context):
    with context.app.app_context():
        from rental_app.cli import search_car
        cli_runner = context.cli_runner
        context.resp = cli_runner.invoke(
            search_car,
            [context.data.get("registration_number")]
        )


@when("I rent Car")
def step_impl(context):
    with context.app.app_context():
        from rental_app.cli import rent
        cli_runner = context.cli_runner
        reg_number = context.data.get("registration_number")
        cust_name = context.rent_data.get("customer_name")
        date = context.rent_data.get("date")
        args = [reg_number, cust_name, date]
        context.resp = cli_runner.invoke(
            rent,
            args
        )


@when("I Check Car Status On {date}")
def step_impl(context, date):
    with context.app.app_context():
        from rental_app.cli import daily_status
        cli_runner = context.cli_runner

        args = [date]
        context.resp = cli_runner.invoke(
            daily_status,
            args
        )


@when("I reserve Car")
def step_impl(context):
    with context.app.app_context():
        from rental_app.cli import rent
        cli_runner = context.cli_runner
        reg_number = context.data.get("registration_number")
        cust_name = context.rent_data.get("customer_name")
        date = context.rent_data.get("date")
        args = [reg_number, cust_name, date]
        context.resp = cli_runner.invoke(
            rent,
            args
        )


@then("I see car saved success")
def step_impl(context):
    if hasattr(context, "resp"):
        result = context.resp
        if not hasattr(result, "output"):
            assert False
        reg_number = context.data.get("registration_number")
        color = context.data.get("color")
        assert f"Car {reg_number} {color} saved" in result.output
    else:
        assert False


@then("I see rent success")
def step_impl(context):
    assert True
    if hasattr(context, "resp"):
        result = context.resp
        if not hasattr(result, "output"):
            assert False
        reg_number = context.data.get("registration_number")
        date = context.rent_data.get("date")
        customer_name = context.rent_data.get("customer_name")
        assert f"Reserved {reg_number} to {customer_name} on {date}" in result.output
    else:
        assert False


@then("I see reserve success")
def step_impl(context):
    assert True
    if hasattr(context, "resp"):
        result = context.resp
        if not hasattr(result, "output"):
            assert False
        reg_number = context.data.get("registration_number")
        date = context.rent_data.get("date")
        customer_name = context.rent_data.get("customer_name")
        assert f"Reserved {reg_number} to {customer_name} on {date}" in result.output
    else:
        assert False


@then("I see listed car")
def step_impl(context):
    if hasattr(context, "resp"):
        result = context.resp
        if not hasattr(result, "output"):
            assert False
        reg_number = context.data.get("registration_number")
        color = context.data.get("color")
        assert result.output.find(reg_number)
        assert result.output.find(color)
    else:
        assert False


@then("I see car status")
def step_impl(context):
    if hasattr(context, "resp"):
        result = context.resp
        if not hasattr(result, "output"):
            assert False
        reg_number = context.data.get("registration_number")
        color = context.data.get("color")
        assert result.output.find(reg_number)
        assert result.output.find(color)
        list_output = result.output.strip().split('\n')
        assert len(list_output) > 1
        list_output.pop(0)
        for output in list_output:
            if output.find(reg_number):
                assert output.find("Rented")
    else:
        assert False

