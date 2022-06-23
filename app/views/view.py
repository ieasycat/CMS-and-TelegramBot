from app import app
from app.controllers.user_db_controller import EmployeeController, ManagerController, UrlController
from app.models.forms import AddEmployeeForm, TechnologyFilterForm, \
    EmployeeSearchForm, RegistrationForm, LoginForm, UpdateEmployeeForm
from flask import render_template, redirect, url_for, Blueprint, request, flash
from flask_login import current_user, login_user, logout_user, login_required
import urllib.parse


mod = Blueprint('employee', __name__, url_prefix='/employee')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def main_page(page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm()
    employees = EmployeeController.get_all_employees(page=page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'next_url': UrlController.get_next_url(endpoint='main_page', pagination=employees),
        'prev_url': UrlController.get_prev_url(endpoint='main_page', pagination=employees)
    }

    form = EmployeeController.form_validate_on_submit(form_filter=form_filter, form_search=form_search)

    if form:
        return form

    return render_template('main.html', context=context)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect((url_for('main_page')))

    if form.validate_on_submit():
        ManagerController.add_manager(form)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('main_page')))

    form = LoginForm()

    if form.validate_on_submit():
        user = ManagerController.get_manager(email=form.email.data)
        check_manager = ManagerController.check_manager(user=user, password=form.password.data)

        if check_manager:
            flash('Invalid username or password')
            return check_manager

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('main_page'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@mod.route('/technology_filter/<string:main_technology>', methods=['GET', 'POST'])
@mod.route('/technology_filter/<string:main_technology>/<int:page>', methods=['GET', 'POST'])
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


@mod.route('/search/<string:name>?<string:last_name>', methods=['GET', 'POST'])
@mod.route('/search/<string:name>?<string:last_name>/<int:page>', methods=['GET', 'POST'])
@login_required
def employee_search(name: str, last_name: str, page=1):
    form_filter = TechnologyFilterForm()
    form_search = EmployeeSearchForm(name=name, last_name=last_name)

    form = EmployeeController.form_validate_on_submit(form_filter=form_filter, form_search=EmployeeSearchForm())

    if form:
        return form

    employees = EmployeeController.employee_search(name=name, last_name=last_name, page=page)
    context = {
        'form_filter': form_filter,
        'form_search': form_search,
        'employees': employees,
        'next_url': UrlController.get_next_url(endpoint='employee.employee_search',
                                               parameter={'name': name, 'last_name': last_name}, pagination=employees),
        'prev_url': UrlController.get_prev_url(endpoint='employee.employee_search',
                                               parameter={'name': name, 'last_name': last_name}, pagination=employees)
    }
    return render_template('employee_search.html', context=context)


@mod.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddEmployeeForm()

    if form.validate_on_submit():
        EmployeeController.add_employee(form=form)
        return redirect(url_for('main_page'))

    return render_template('add_employee.html', form=form)


@mod.route('/update/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def update_user(employee_id: int):
    employee = EmployeeController.get_employee(employee_id)

    form = UpdateEmployeeForm(**employee.__dict__,
                              cv=employee.employee_data.cv,
                              additional_data=employee.employee_data.additional_data)

    if form.validate_on_submit():
        EmployeeController.update_employee(user=employee, form=form)
        return redirect(url_for('main_page'))

    return render_template('update_employee.html', form=form)


@mod.route('/update_status/<int:employee_id>', methods=['POST'])
@login_required
def update_status(employee_id: int):
    EmployeeController.change_status(employee_id)
    return redirect(request.headers['Referer'])


@mod.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete_user(employee_id: int):
    EmployeeController.delete_employee(employee_id)
    return redirect(request.headers['Referer'])
