from app import db
from app.controllers.employee_db_controller import EmployeeController
from app.models.dbmodels import Employee
from app.models.forms import UpdateEmployeeForm, AddEmployeeForm


def test_get_all_employees(employee):
    employees = EmployeeController.get_all_employees(page=1)
    assert employees.total == 1


def test_technology_filter(employee):
    employees = EmployeeController.technology_filter(main_technology='Python', page=1)
    assert employees.total == 1


def test_employee_search(employee):
    employees = EmployeeController.employee_search(data='Test', page=1)
    assert employees.total == 1


def test_change_status(employee):
    EmployeeController.change_status(employee_id=employee.id)
    assert employee.status == 'Busy'


def test_add_employee(app):
    test_form = AddEmployeeForm(
        name='Test1',
        last_name='Tester1',
        main_technology='Python',
        status='Free',
        cv='Testing'
    )
    EmployeeController.add_employee(test_form)

    assert db.session.query(Employee).filter_by(name='Test1').first().name == 'Test1'


def test_update_employee(employee):
    test_form = UpdateEmployeeForm(**employee.__dict__)
    test_form.name.data, test_form.status.data = 'Update', 'Busy'
    EmployeeController.update_employee(employee=employee, form=test_form)
    assert employee.name == 'Update' and employee.status == 'Busy'


def test_delete_employee(employee):
    EmployeeController.delete_employee(employee_id=employee.id)
    assert not EmployeeController.get_employee(employee.id)
