from app.controllers.employee_db_controller import EmployeeController
from app.controllers.url_controller import UrlController
from app.models.forms import AddEmployeeForm, TechnologyFilterForm, EmployeeSearchForm, UpdateEmployeeForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required
import urllib.parse
from app.views import main, bp


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm()
    employees = EmployeeController.get_all_employees(page=page)
    weather_loc_info, weather_info = UrlController.weather_request()

    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'next_url': UrlController.get_next_url(endpoint='main.index', pagination=employees),
        'prev_url': UrlController.get_prev_url(endpoint='main.index', pagination=employees),
        'weather_loc_info': weather_loc_info,
        'weather_info': weather_info
    }

    form = EmployeeController.form_validate_on_submit(form_filter=form_filter, form_search=form_search)

    if form:
        return form

    return render_template('main.html', context=context)


@bp.route('/technology_filter/<string:main_technology>', methods=['GET', 'POST'])
@bp.route('/technology_filter/<string:main_technology>/<int:page>', methods=['GET', 'POST'])
@login_required
def technology_filter(main_technology: str, page=1):
    form_filter = TechnologyFilterForm(main_technology=urllib.parse.unquote(main_technology))
    form_search = EmployeeSearchForm()

    form = EmployeeController.form_validate_on_submit(form_filter=TechnologyFilterForm(), form_search=form_search)

    if form:
        return form

    employees = EmployeeController.technology_filter(urllib.parse.unquote(main_technology), page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'next_url': UrlController.get_next_url(endpoint='employee.technology_filter',
                                               parameter={'main_technology': main_technology}, pagination=employees),
        'prev_url': UrlController.get_prev_url(endpoint='employee.technology_filter',
                                               parameter={'main_technology': main_technology}, pagination=employees)
    }
    return render_template('technology_filter.html', context=context)


@bp.route('/search/<string:data>', methods=['GET', 'POST'])
@bp.route('/search/<string:data>/<int:page>', methods=['GET', 'POST'])
@login_required
def employee_search(data: str, page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm(search=data)

    form = EmployeeController.form_validate_on_submit(form_filter=form_filter, form_search=EmployeeSearchForm())

    if form:
        return form

    employees = EmployeeController.employee_search(data=data, page=page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'next_url': UrlController.get_next_url(endpoint='employee.employee_search',
                                               parameter={'data': data}, pagination=employees),
        'prev_url': UrlController.get_prev_url(endpoint='employee.employee_search',
                                               parameter={'data': data}, pagination=employees)
    }
    return render_template('employee_search.html', context=context)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddEmployeeForm()

    if form.validate_on_submit():
        EmployeeController.add_employee(form=form)
        return redirect(url_for('main.index'))

    return render_template('add_employee.html', form=form)


@bp.route('/update/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def update_user(employee_id: int):
    employee = EmployeeController.get_employee(employee_id)

    form = UpdateEmployeeForm(**employee.__dict__,
                              cv=employee.employee_data.cv,
                              additional_data=employee.employee_data.additional_data)

    if form.validate_on_submit():
        EmployeeController.update_employee(employee=employee, form=form)
        return redirect(url_for('main.index'))

    return render_template('update_employee.html', form=form)


@bp.route('/update_status/<int:employee_id>', methods=['POST'])
@login_required
def update_status(employee_id: int):
    EmployeeController.change_status(employee_id)
    return redirect(request.headers['Referer'])


@bp.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete_user(employee_id: int):
    EmployeeController.delete_employee(employee_id)
    return redirect(request.headers['Referer'])
