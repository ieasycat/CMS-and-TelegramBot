from app.api import bp
from app.controllers.api_controller import ApiController
from flask import jsonify, request
from app.api.errors import bad_request


@bp.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(ApiController.get_all_employees())


@bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id: int):
    return jsonify(ApiController.get_employee(employee_id))


@bp.route('employees/filter', methods=['GET'])
def technology_filter():
    data = request.get_json() or {}
    if 'main_technology' not in data:
        return bad_request('must include main technology fields')
    return jsonify(ApiController.technology_filter(data))


@bp.route('employees/search', methods=['GET'])
def employee_search():
    data = request.get_json() or {}
    if 'name' not in data or 'last_name' not in data:
        return bad_request('must include name and last name fields')
    return jsonify(ApiController.employee_search(data))


@bp.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json() or {}
    if 'name' not in data or 'last_name' not in data or 'main_technology' not in data or 'status' not in data:
        return bad_request('must include name, last name, main technology and status fields')
    ApiController.add_employee(data)
    return jsonify({'status': 'success'})


@bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id: int):
    data = request.get_json() or {}
    ApiController.update_employee(data, employee_id)
    return jsonify({'status': 'success'})


@bp.route('/employees/update_status/<int:employee_id>', methods=['PUT'])
def update_status(employee_id: int):
    ApiController.update_status(employee_id)
    return jsonify({'status': 'success'})


@bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id: int):
    ApiController.delete_employee(employee_id)
    return jsonify({'status': 'success'})
