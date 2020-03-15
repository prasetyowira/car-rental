"""
This file handle index's blueprints
"""
from rental_app.tools.commons import make_json_response
from flask import Blueprint, Response

index_blueprint = Blueprint("index", __name__, url_prefix="/")


@index_blueprint.route("", methods=("GET",))
def index() -> Response:  # pragma: no cover
    """
    This method response hello world in / path

    Returns:
        [Response] -- [flask Response object]
    """

    return make_json_response(http_status=200, data={"message": "Hello, World!"})
