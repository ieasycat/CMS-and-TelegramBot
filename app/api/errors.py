from flask import jsonify
from app.api import bp
from app.api.models.employee_models import APIError
from flask import Response


@bp.errorhandler(APIError)
def invalid_api_validation(e: APIError) -> Response:
    return jsonify(e.to_dict())
