def test_camel_case():
    from rental_app.tools.commons import camelcase

    sample_words = ["sample", "snake_case"]
    output = list()
    for wods in sample_words:
        output.append(camelcase(wods))

    expected = ["sample", "snakeCase"]
    assert output == expected


def test_enum_comprehensions():
    from rental_app.tools.commons import enum_comprehensions
    from rental_app.enums import CarStatusStatus

    results = enum_comprehensions(CarStatusStatus)
    expected = ["Free", "Rented", "In Repair"]
    assert results == expected
