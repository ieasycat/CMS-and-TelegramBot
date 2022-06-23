from app import db
from app.models.dbmodels import Manager, Employee, EmployeeData
from app.models.forms import AddEmployeeForm, TechnologyFilterForm, EmployeeSearchForm, RegistrationForm
from flask import redirect, url_for
from flask_sqlalchemy import Pagination
from sqlalchemy import and_
from config import CONFIG
import urllib.parse
from werkzeug.wrappers.response import Response


class EmployeeController:

    @staticmethod
    def get_all_employees(page: int) -> Pagination:
        return db.session.query(Employee).order_by(Employee.id).paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def get_employee(employee_id: int) -> Employee:
        return db.session.query(Employee).filter_by(id=employee_id).first()

    @staticmethod
    def technology_filter(main_technology: str, page: int) -> Pagination:
        return db.session.query(Employee).filter_by(main_technology=main_technology).\
            order_by(Employee.id).paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def employee_search(name: str, last_name: str, page: int) -> Pagination:
        return db.session.query(Employee).filter(and_(
            Employee.name == name, Employee.last_name == last_name)).\
            order_by(Employee.id).paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def change_status(employee_id: int):
        try:
            db.session.query(Employee).filter_by(id=employee_id).first().change_status()
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def add_employee(form: AddEmployeeForm):
        try:
            user = Employee(
                name=form.name.data,
                last_name=form.last_name.data,
                main_technology=form.main_technology.data,
                status=form.status.data,
            )

            db.session.add(user)
            db.session.flush()
            user.generate_nickname()

            user_data = EmployeeData(
                cv=form.cv.data,
                additional_data=form.additional_data.data,
                employee_id=user.id
            )

            db.session.add(user_data)
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def update_employee(user: Employee, form: AddEmployeeForm):
        try:
            user.name = form.name.data
            user.last_name = form.last_name.data
            user.main_technology = form.main_technology.data
            user.status = form.status.data
            user.employee_data.cv = form.cv.data
            user.employee_data.additional_data = form.additional_data.data
            db.session.flush()

            db.session.commit()

        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def delete_employee(employee_id: int):
        try:
            Employee.query.filter_by(id=employee_id).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def form_validate_on_submit(form_filter: TechnologyFilterForm, form_search: EmployeeSearchForm) -> Response:
        if form_filter.validate_on_submit():
            main_technology = urllib.parse.quote(form_filter.main_technology.data, safe='')
            return redirect(url_for('employee.technology_filter', main_technology=main_technology))

        if form_search.validate_on_submit():
            name = form_search.name.data
            last_name = form_search.last_name.data
            return redirect(url_for('employee.employee_search', name=name, last_name=last_name))


class ManagerController:

    @staticmethod
    def add_manager(form: RegistrationForm):
        try:
            user = Manager(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def get_manager(email: str) -> Manager:
        return db.session.query(Manager).filter_by(email=email).first()

    @staticmethod
    def check_manager(user: Manager, password: str) -> Response:
        if user is None or not user.check_password(password):
            return redirect(url_for('login'))


class UrlController:

    @staticmethod
    def get_next_url(endpoint: str, pagination: Pagination, parameter=None) -> str or None:
        if parameter:
            return url_for(endpoint, **parameter, page=pagination.next_num) if pagination.has_next else None
        else:
            return url_for(endpoint, page=pagination.next_num) if pagination.has_next else None

    @staticmethod
    def get_prev_url(endpoint: str, pagination: Pagination, parameter=None) -> str or None:
        if parameter:
            return url_for(endpoint, **parameter, page=pagination.prev_num) if pagination.has_prev else None
        else:
            return url_for(endpoint, page=pagination.prev_num) if pagination.has_prev else None
