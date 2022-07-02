from app import app
from app.controllers.user_db_controller import EmployeeController
from flask import render_template, redirect, url_for, Blueprint, request
from app.models.forms import AddEmployeeForm, TechnologyFilterForm, EmployeeSearchForm
import urllib.parse


mod = Blueprint('employee', __name__, url_prefix='/employee')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def main_page(page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm()
    employees = EmployeeController.get_all_employees(page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
    }

    if form_filter.validate_on_submit():
        main_technology = urllib.parse.quote(form_filter.main_technology.data, safe='')
        return redirect(url_for('employee.technology_filter', main_technology=main_technology))

    if form_search.validate_on_submit():
        name = form_search.name.data
        last_name = form_search.last_name.data
        return redirect(url_for('employee.search', name=name, last_name=last_name))

    return render_template('main.html', context=context)


@mod.route('/technology_filter/<string:main_technology>', methods=['GET', 'POST'])
@mod.route('/technology_filter/<string:main_technology>/<int:page>', methods=['GET', 'POST'])
def technology_filter(main_technology: str, page=1):
    form_filter = TechnologyFilterForm(main_technology=urllib.parse.unquote(main_technology))
    form_search = EmployeeSearchForm()

    if form_filter.validate_on_submit():
        main_technology = urllib.parse.quote(form_filter.main_technology.data, safe='')
        return redirect(url_for('employee.technology_filter', main_technology=main_technology))

    if form_search.validate_on_submit():
        name = form_search.name.data
        last_name = form_search.last_name.data
        return redirect(url_for('employee.search', name=name, last_name=last_name))

    employees = EmployeeController.technology_filter(urllib.parse.unquote(main_technology), page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'main_technology': main_technology
    }
    return render_template('technology_filter.html', context=context)


@mod.route('/search/<string:name>?<string:last_name>', methods=['GET', 'POST'])
@mod.route('/search/<string:name>?<string:last_name>/<int:page>', methods=['GET', 'POST'])
def employee_search(name: str, last_name: str, page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm(name=name, last_name=last_name)

    if form_filter.validate_on_submit():
        main_technology = urllib.parse.quote(form_filter.main_technology.data, safe='')
        return redirect(url_for('employee.technology_filter', main_technology=main_technology))

    if form_search.validate_on_submit():
        name = form_search.name.data
        last_name = form_search.last_name.data
        return redirect(url_for('employee.search', name=name, last_name=last_name))

    employees = EmployeeController.employee_search(name=name, last_name=last_name, page=page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'name': name,
        'last_name': last_name
    }
    return render_template('employee_search.html', context=context)


@mod.route('/get/<int:employee_id>', methods=['GET', 'POST'])
def get_user(employee_id: int):
    return render_template('employee_info.html', employee=EmployeeController.get_employee(employee_id))


@mod.route('/add', methods=['GET', 'POST'])
def add_user():
    form = AddEmployeeForm()

    if form.validate_on_submit():
        EmployeeController.add_employee(form=form)
        return redirect(url_for('main_page'))

    return render_template('add_employee.html', form=form)


@mod.route('/update/<int:employee_id>', methods=['GET', 'POST'])
def update_user(employee_id: int):
    employee = EmployeeController.get_employee(employee_id)

    form = AddEmployeeForm(**employee.__dict__,
                           cv=employee.employee_data.cv,
                           additional_data=employee.employee_data.additional_data)

    if form.validate_on_submit():
        EmployeeController.update_employee(user=employee, form=form)
        return redirect(url_for('main_page'))

    return render_template('update_employee.html', form=form)


@mod.route('/update_status/<int:employee_id>', methods=['POST'])
def update_status(employee_id: int):
    EmployeeController.change_status(employee_id)
    return redirect(request.headers['Referer'])


@mod.route('/delete/<int:employee_id>', methods=['POST'])
def delete_user(employee_id: int):
    EmployeeController.delete_employee(employee_id)
    return redirect(request.headers['Referer'])
