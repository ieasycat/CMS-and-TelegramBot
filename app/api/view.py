from app.api import bp
from app.api.controllers.employee_db_controller import ApiController
from app.api.models.employee_models import EmployeeAddRequest, EmployeeUpdateRequest, EmployeeFilterRequest, \
    EmployeeSearchRequest, ResponseModel, GetEmployeesResponse
from app.api.authorization import token_auth
from app.api.errors import APIError
from dataclass_type_validator import TypeValidationError
from flask import jsonify, request, make_response


@bp.route('/employees', methods=['GET'])
@token_auth.login_required
def get_employees():
    return make_response(jsonify(GetEmployeesResponse(ApiController.get_all_employees())), 200)


@bp.route('/employees/<int:employee_id>', methods=['GET'])
@token_auth.login_required
def get_employee(employee_id: int):
    return make_response(jsonify(ApiController.get_employee(employee_id=employee_id)), 200)


@bp.route('employees/filter', methods=['GET'])
@token_auth.login_required
def technology_filter():
    json = request.get_json()
    try:
        data = EmployeeFilterRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    return make_response(jsonify(ApiController.technology_filter(data=data)), 200)


@bp.route('employees/search', methods=['GET'])
@token_auth.login_required
def employee_search():
    json = request.get_json()
    try:
        data = EmployeeSearchRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    return make_response(jsonify(ApiController.employee_search(data=data)), 200)


@bp.route('/employees', methods=['POST'])
@token_auth.login_required
def add_employee():
    json = request.get_json()
    try:
        data = EmployeeAddRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    ApiController.add_employee(data=data)
    return make_response(jsonify(ResponseModel.response_created()), 201)


@bp.route('/employees/<int:employee_id>', methods=['PUT'])
@token_auth.login_required
def update_employee(employee_id: int):
    json = request.get_json()
    try:
        data = EmployeeUpdateRequest(**json)
    except TypeValidationError as e:
        raise APIError(message=e.errors)
    ApiController.update_employee(data=data, employee_id=employee_id)
    return make_response(jsonify(ResponseModel.response_ok()), 200)


@bp.route('/employees/update_status/<int:employee_id>', methods=['PUT'])
@token_auth.login_required
def update_status(employee_id: int):
    ApiController.update_status(employee_id=employee_id)
    return make_response(jsonify(ResponseModel.response_ok()), 200)


@bp.route('/employees/<int:employee_id>', methods=['DELETE'])
@token_auth.login_required
def delete_employee(employee_id: int):
    ApiController.delete_employee(employee_id=employee_id)
    return make_response(jsonify(ResponseModel.response_ok()), 200)
