from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_
from app.models.dbmodels import Employee, EmployeeData
from app.api.models.employee_models import EmployeeResponse, EmployeeAddRequest, EmployeeSearchRequest, \
    EmployeeFilterRequest, EmployeeUpdateRequest
from app import db


class ApiController:

    @classmethod
    def get_all_employees(cls) -> list:
        return cls.to_list(Employee.query.all())

    @staticmethod
    def get_employee(employee_id: int) -> dict:
        employee = Employee.query.get_or_404(employee_id).__dict__
        employee.pop('_sa_instance_state')
        return employee

    @staticmethod
    def add_employee(data: EmployeeAddRequest):
        try:
            employee = Employee(
                name=data.name.capitalize(),
                last_name=data.last_name.capitalize(),
                main_technology=data.main_technology,
                status=data.status.capitalize()
            )

            db.session.add(employee)
            db.session.flush()
            employee.generate_nickname()

            employee_data = EmployeeData(
                cv=data.cv,
                additional_data=data.additional_data,
                employee_id=employee.id
            )

            db.session.add(employee_data)
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def update_employee(data: EmployeeUpdateRequest, employee_id: int):
        try:
            employee = Employee.query.get(employee_id)
            employee.name = data.name.capitalize()
            employee.last_name = data.last_name.capitalize()
            employee.main_technology = data.main_technology
            employee.status = data.status.capitalize()
            employee.employee_data.cd = data.cv
            employee.employee_data.additional_data = data.additional_data

            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def update_status(employee_id: int):
        try:
            employee = Employee.query.get(employee_id)
            employee.change_status()

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

    @classmethod
    def technology_filter(cls, data: EmployeeFilterRequest) -> list:
        return cls.to_list(Employee.query.filter_by(main_technology=data.main_technology))

    @classmethod
    def employee_search(cls, data: EmployeeSearchRequest) -> list:
        return cls.to_list(
            Employee.query.filter(
                or_(
                    Employee.name.like(f'%{data.data}%'),
                    Employee.nickname.like(f'%{data.data}%'),
                    Employee.last_name.like(f'%{data.data}%')
                )
            )
        )

    @staticmethod
    def to_list(employees: BaseQuery) -> list:
        return [EmployeeResponse(id=el.id,
                                 name=el.name,
                                 last_name=el.last_name,
                                 nickname=el.nickname,
                                 main_technology=el.main_technology,
                                 status=el.status,
                                 cv=el.employee_data.cv,
                                 additional_data=el.employee_data.additional_data) for el in employees]
