import logging
from logging.config import dictConfig

import yaml
from flask import request


with open(r"server/logger.yaml") as fp:
    custom_format = yaml.safe_load(fp)


def get_request_string(status):
    return "{0} - {1}:{2} {3} {4}?{5} {6} -".format(
        status,
        request.environ["REMOTE_ADDR"],
        request.environ["REMOTE_PORT"],
        request.environ["REQUEST_METHOD"],
        request.environ["PATH_INFO"],
        request.environ["QUERY_STRING"],
        request.environ["SERVER_PROTOCOL"],
    )


def logger_citenote(response):
    dictConfig(custom_format)
    status = response.status_code

    if 300 <= status < 400:
        logging.warning(get_request_string(status))

    if 400 <= status:
        logging.error(get_request_string(status))

    return response


if __name__ == "__main__":
    raise ConnectionRefusedError
