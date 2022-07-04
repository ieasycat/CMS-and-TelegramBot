from app import db
from app.models.dbmodels import Employee, EmployeeData
from app.models.forms import AddEmployeeForm, TechnologyFilterForm, EmployeeSearchForm
from flask import redirect, url_for, current_app
from flask_sqlalchemy import Pagination
from sqlalchemy import or_
import urllib.parse
from werkzeug.wrappers.response import Response


class EmployeeController:

    @staticmethod
    def get_all_employees(page: int) -> Pagination:
        return db.session.query(Employee).order_by(Employee.id).\
            paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    @staticmethod
    def get_employee(employee_id: int) -> Employee:
        return db.session.query(Employee).filter_by(id=employee_id).first()

    @staticmethod
    def technology_filter(main_technology: str, page: int) -> Pagination:
        return db.session.query(Employee).filter_by(main_technology=main_technology).\
            order_by(Employee.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    @staticmethod
    def employee_search(data: str, page: int) -> Pagination:
        return db.session.query(Employee).filter(or_(
            Employee.name.like(f'{data.capitalize()}%'),
            Employee.nickname.like(f'{data.capitalize()}%'),
            Employee.last_name.like(f'{data.capitalize()}%')
        )
        ).order_by(Employee.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

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
                name=form.name.data.capitalize(),
                last_name=form.last_name.data.capitalize(),
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
            user.name = form.name.data.capitalize()
            user.last_name = form.last_name.data.capitalize()
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
            data = form_search.search.data
            return redirect(url_for('employee.employee_search', data=data))
