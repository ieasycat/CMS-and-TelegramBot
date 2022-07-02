from sqlalchemy import and_
from app.models.dbmodels import Employee, EmployeeData
from app import db
from config import CONFIG
from flask import redirect, url_for
import urllib.parse

from app.models.forms import AddEmployeeForm, TechnologyFilter, EmployeeSearch
from flask_sqlalchemy import Pagination
from werkzeug.wrappers.response import Response


class EmployeeController:

    @staticmethod
    def get_all_employees(page: int) -> Pagination:
        return db.session.query(Employee).order_by(Employee.id).paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def get_employee(employee_id: int) -> Employee:
        return db.session.query(Employee).filter(Employee.id == employee_id).first()

    @staticmethod
    def technology_filter(main_technology: str, page: int) -> Pagination:
        return db.session.query(Employee).filter(Employee.main_technology == main_technology).\
            paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def employee_search(name: str, last_name: str, page: int) -> Pagination:
        return db.session.query(Employee).filter(and_(
            Employee.name == name, Employee.last_name == last_name)).\
            paginate(page, CONFIG.POSTS_PER_PAGE, False)

    @staticmethod
    def change_status(employee_id: int):
        try:
            db.session.query(Employee).filter(Employee.id == employee_id).first().change_status()
            db.session.commit()
            db.session.close()
        except Exception:
            db.session.rollback()

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
            db.session.close()
        except Exception:
            db.session.rollback()

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
            db.session.close()
        except Exception:
            db.session.rollback()

    @staticmethod
    def delete_employee(employee_id: int):
        try:
            Employee.query.filter(Employee.id == employee_id).delete()
            db.session.commit()
            db.session.close()
        except Exception:
            db.session.rollback()

    @staticmethod
    def form_validate_on_submit(form_filter: TechnologyFilter, form_search: EmployeeSearch) -> Response:
        if form_filter.validate_on_submit():
            main_technology = urllib.parse.quote(form_filter.main_technology.data, safe='')
            return redirect(url_for('employee.technology_filter', main_technology=main_technology))

        if form_search.validate_on_submit():
            name = form_search.name.data
            last_name = form_search.last_name.data
            return redirect(url_for('employee.employee_search', name=name, last_name=last_name))
