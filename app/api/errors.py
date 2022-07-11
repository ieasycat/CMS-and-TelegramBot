from http import HTTPStatus
from flask import jsonify
from app.api import bp
from flask import Response


class APIError(Exception):
    def __init__(self, message: dict, code: HTTPStatus = HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.code = code


@bp.errorhandler(APIError)
def invalid_api_validation(e: APIError) -> Response:
    return jsonify(e.__dict__)
