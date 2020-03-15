"""
This file is the init file that provide method to create a modified flask app
"""
import http
import json
import locale
import os
from logging import getLogger
from typing import Any

from celery import Celery
from flask import Flask, Response, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from .cli import (car_cli, rent_cli, )
from .tools.commons import (
    descripted_exception_logger,
    discover_blueprints,
    make_json_response,
)

app_logger = getLogger("app")
error_logger = getLogger("error")
access_logger = getLogger("access")

try:
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
except locale.Error as e:
    error_logger.error(f"LOCALE ERROR: {e}")
    pass

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def resource_not_found(e: Any = "Not Found") -> Response:
    """
    This method is a error handler for http status Not Found

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Not Found"})

    Returns:
        [Response] -- [404 Response]
    """
    # return jsonify({"code": 404, "message": str(e)}), http.HTTPStatus.NOT_FOUND
    return make_json_response(http_status=404, data={"code": 404, "message": str(e)})


def unauthorized(e: Any = "Unauthorized") -> Response:
    """
    This method is a error handler for http status Unauthorized

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Unauthorized"})

    Returns:
        [Response] -- [401 Response]
    """
    # return jsonify({"code": 401, "message": str(e)}), http.HTTPStatus.UNAUTHORIZED
    return make_json_response(http_status=401, data={"code": 401, "message": str(e)})


def forbidden(e: Any = "Forbidden") -> Response:
    """
    This method is a error handler for http status Forbidden

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Forbidden"})

    Returns:
        [Response] -- [403 Response]
    """
    # return jsonify({"code": 403, "message": str(e)}), http.HTTPStatus.FORBIDDEN
    return make_json_response(http_status=403, data={"code": 403, "message": str(e)})


def method_not_allowed(e: Any = "Method Not Allowed") -> Response:
    """
    This method is a error handler for http status Method Not Allowed

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Method Not Allowed"})

    Returns:
        [Response] -- [403 Response]
    """
    # return jsonify({"code": 405, "message": str(e)}), http.HTTPStatus.METHOD_NOT_ALLOWED
    return make_json_response(http_status=405, data={"code": 405, "message": str(e)})


def handle_options_method() -> Any:
    """
    This method used to handle options method from front end

    Returns:
        Any -- [Return 204 if method is OPTIONS else return the original request]
    """
    if request.method == "OPTIONS":
        return Response(status=http.HTTPStatus.NO_CONTENT)


def exception_handler(e: Exception) -> Response:
    """
    This method used to handle unhandled exception

    Arguments:
        e {Exception} -- [Exception object]

    Returns:
        Response -- [Return internal server error message]
    """
    descripted_exception_logger(e)

    return Response(
        response=json.dumps({"code": 500, "message": "Internal Server Error"}),
        status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        mimetype="application/json",
    )


def after_request(response: Response) -> Response:
    """
    This method used to handle access log

    Arguments:
        response {Response} -- [The flask Response object]

    Returns:
        Response -- [Flask response object that passed to parameter]
    """
    try:
        access_logger = getLogger("access")
        request_method = request.method
        request_headers = dict(request.headers)
        request_url = f"{request.scheme}://{request.remote_addr}{request.full_path}"
        request_payload = json.loads(request.get_json()) if request.get_json() else "{}"

        response_headers = dict(response.headers)
        response_payload = json.loads(response.response[0])
        response_status = response.status
        message = (
            f"{request_method} | {request_url} | {response_status} | {request_headers} "
            f"| {request_payload} | {response_headers} | {response_payload}"
        )
        access_logger.info(message)
    except Exception as e:
        exception_handler(e)

    return response


def create_app(test: bool = False) -> Flask:
    """
    This method used to handle app creation and configure some objects

    Keyword Arguments:
        test {bool} -- [The test flag to distinguish between main app and test app] (default: {False})

    Returns:
        Flask -- [Configured Flask App]
    """
    app = Flask(__name__, instance_relative_config=False)

    if test:
        app.config.from_object("rental_app.config.TestConfig")
    else:
        app.config.from_object("rental_app.config.Config")

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    register_commands(app)
    blueprints = discover_blueprints(os.path.dirname(os.path.abspath(__file__)))

    with app.app_context():
        for blueprint in blueprints:
            try:
                app.register_blueprint(blueprint)
            except Exception as e:
                error_logger.error(f"Failed to register blueprint {blueprint}: {e}")

        app.url_map.strict_slashes = True

        app.before_request(handle_options_method)
        app.after_request(after_request)

        app.register_error_handler(Exception, exception_handler)
        app.register_error_handler(http.HTTPStatus.NOT_FOUND, resource_not_found)
        app.register_error_handler(http.HTTPStatus.UNAUTHORIZED, unauthorized)
        app.register_error_handler(http.HTTPStatus.FORBIDDEN, forbidden)
        app.register_error_handler(
            http.HTTPStatus.METHOD_NOT_ALLOWED, method_not_allowed
        )

        return app


def make_celery(app=None):
    app = app or create_app()
    celery_instance = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask
    return celery_instance


def make_redis_client(app=None):
    redis = Redis(
        app.config["REDIS_HOST"],
        app.config["REDIS_PORT"],
        app.config["MASTER_REDIS_DB"],
    )
    return redis


def register_commands(app: Flask):
    """Register Click commands."""
    app.cli.add_command(car_cli)
    app.cli.add_command(rent_cli)
