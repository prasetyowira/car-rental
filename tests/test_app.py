from rental_app import create_app


def test_create_app():
    assert create_app(test=True)
    assert create_app()
