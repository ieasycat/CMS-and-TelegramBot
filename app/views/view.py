from app import app
from app.controllers.user_db_controller import EmployeeController
from flask import render_template, redirect, url_for, Blueprint
from app.models.forms import AddEmployeeForm


mod = Blueprint('employee', __name__, url_prefix='/employee')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def main_page(page=1):
    employees = EmployeeController.get_all_employees(page)
    return render_template('main_page.html', employees=employees)


@mod.route('/get/<int:employee_id>', methods=['GET', 'POST'])
def get_user(employee_id: int):
    return render_template('employee_info_page.html', employee=EmployeeController.get_employee(employee_id))


@mod.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddEmployeeForm()

    if form.validate_on_submit():
        EmployeeController.add_employee(form=form)
        return redirect(url_for('main_page'))

    return render_template('add_page.html', form=form)


@mod.route('/update/<int:employee_id>', methods=['GET', 'POST'])
def update_user(employee_id: int):
    employee = EmployeeController.get_employee(employee_id)

    form = AddEmployeeForm(**employee.__dict__)

    if form.validate_on_submit():
        EmployeeController.update_employee(user=employee, form=form)
        return redirect(url_for('main_page'))

    return render_template('update_user.html', form=form)


@mod.route('/update_status/<int:employee_id>', methods=['POST'])
def update_status(employee_id: int):
    EmployeeController.change_status(employee_id)
    return redirect(url_for('main_page'))


@mod.route('/delete/<int:employee_id>', methods=['POST'])
def delete_user(employee_id: int):
    EmployeeController.delete_employee(employee_id)
    return redirect(url_for('main_page'))
