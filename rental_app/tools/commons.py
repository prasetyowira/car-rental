"""
This file contains the common tools
"""
import base64
import importlib
import json
import mimetypes
import os
import traceback
from http import HTTPStatus
from logging import getLogger
from typing import Union

import requests
from flask import Response, current_app

error_logger = getLogger("error")


def discover_blueprints(path: str) -> list:
    """
    This method used to load blueprints from given path

    Arguments:
        path {str} -- [The path that contains blueprints module]

    Returns:
        list -- [The list of blueprints object]
    """
    blueprints = list()
    dir_name = os.path.basename(path)
    packages = os.listdir(f"{path}/blueprints")

    for package in packages:
        if str(package).endswith(".py") and str(package) != "__init__.py":
            package = str(package).replace(".py", "")
            module_name = f"{dir_name}.blueprints.{package}"
            module = importlib.import_module(module_name)
            module_blueprints = [bp for bp in dir(module) if bp.endswith("_blueprint")]

            for mb in module_blueprints:
                blueprints.append(getattr(module, mb))

    return blueprints


def make_json_response(http_status: Union[HTTPStatus, int], data: dict) -> Response:
    """
    This method used to make flask Response object from given http status and response data

    Arguments:
        http_status {Union[HTTPStatus, int]} -- [The HTTP status to be returned]
        data {dict} -- [The response data]

    Returns:
        Response -- [flask Response object]
    """
    return Response(
        response=json.dumps(data), status=http_status, mimetype="application/json"
    )


def descripted_exception_logger(e: Exception) -> None:
    """
    This method used to log an exception with description

    Arguments:
        e {Exception} -- [The raised exception]
    """
    tb_frames = traceback.extract_tb(e.__traceback__)
    message = list()
    pardir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    for tb in tb_frames:
        if tb.filename.startswith(pardir_name):
            message.append(f"{e} in {tb.filename} line number {tb.lineno}")
    error_logger.error(",".join(message))


def camelcase(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def enum_comprehensions(enum):
    return [str(key.value) for key in enum]

