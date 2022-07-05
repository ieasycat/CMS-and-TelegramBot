from app.api import bp
from app.api.controllers.employee_controller import ApiController
from app.api.models.employee_models import EmployeeAddRequest, EmployeeUpdateRequest, EmployeeFilterRequest, \
    EmployeeSearchRequest, ResponseModel
from app.api.authorization import auth
from app.api.errors import APIError
from dataclass_type_validator import TypeValidationError
from flask import jsonify, request


@bp.route('/employees', methods=['GET'])
@auth.login_required
def get_employees():
    return jsonify(ApiController.get_all_employees())


@bp.route('/employees/<int:employee_id>', methods=['GET'])
@auth.login_required
def get_employee(employee_id: int):
    return jsonify(ApiController.get_employee(employee_id=employee_id))


@bp.route('employees/filter', methods=['GET'])
@auth.login_required
def technology_filter():
    json = request.get_json()
    try:
        data = EmployeeFilterRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    return jsonify(ApiController.technology_filter(data=data))


@bp.route('employees/search', methods=['GET'])
@auth.login_required
def employee_search():
    json = request.get_json()
    try:
        data = EmployeeSearchRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    return jsonify(ApiController.employee_search(data=data))


@bp.route('/employees', methods=['POST'])
@auth.login_required
def add_employee():
    json = request.get_json()
    try:
        data = EmployeeAddRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    ApiController.add_employee(data=data)
    return jsonify(ResponseModel.response_ok())


@bp.route('/employees/<int:employee_id>', methods=['PUT'])
@auth.login_required
def update_employee(employee_id: int):
    json = request.get_json()
    try:
        data = EmployeeUpdateRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    ApiController.update_employee(data=data, employee_id=employee_id)
    return jsonify(ResponseModel.response_ok())


@bp.route('/employees/update_status/<int:employee_id>', methods=['PUT'])
@auth.login_required
def update_status(employee_id: int):
    ApiController.update_status(employee_id=employee_id)
    return jsonify(ResponseModel.response_ok())


@bp.route('/employees/<int:employee_id>', methods=['DELETE'])
@auth.login_required
def delete_employee(employee_id: int):
    ApiController.delete_employee(employee_id=employee_id)
    return jsonify(ResponseModel.response_ok())
