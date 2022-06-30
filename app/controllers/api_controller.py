from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_
from app.models.dbmodels import Employee, EmployeeData
from app import db


class ApiController:

    @classmethod
    def get_all_employees(cls) -> dict:
        return cls.to_collection_dict(Employee.query)

    @classmethod
    def get_employee(cls, employee_id: int) -> dict:
        return cls.to_dict(Employee.query.get_or_404(employee_id))

    @staticmethod
    def add_employee(data: dict):
        try:
            employee = Employee(
                name=data['name'].capitalize(),
                last_name=data['last_name'].capitalize(),
                main_technology=data['main_technology'].capitalize(),
                status=data['status'].capitalize()
            )

            db.session.add(employee)
            db.session.flush()
            employee.generate_nickname()

            employee_data = EmployeeData(
                cv=data['cv'] if 'cv' in data else '',
                additional_data=data['additional_data'] if 'additional_data' in data else '',
                employee_id=employee.id
            )

            db.session.add(employee_data)
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def update_employee(data: dict, employee_id: int):
        try:
            employee = Employee.query.get(employee_id)
            employee.name = data['name'].capitalize() if 'name' in data else employee.name
            employee.last_name = data['last_name'].capitalize() if 'last_name' in data else employee.last_name
            employee.main_technology = data['main_technology'].capitalize() if 'main_technology' in data \
                else employee.main_technology
            employee.status = data['status'].capitalize() if 'status' in data else employee.status
            employee.employee_data.cd = data['cv'] if 'cv' in data else employee.employee_data.cv
            employee.employee_data.additional_data = data['additional_data'] if 'additional_data' in data \
                else employee.employee_data.additional_data

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
    def technology_filter(cls, data: dict) -> dict:
        return cls.to_collection_dict(
            Employee.query.filter_by(main_technology=data['main_technology'].capitalize())
        )

    @classmethod
    def employee_search(cls, data: dict) -> dict:
        print(data)
        return cls.to_collection_dict(
            Employee.query.filter(
                or_(
                    Employee.name == data['name'].capitalize() if 'name' in data else None,
                    Employee.last_name == data['last_name'].capitalize() if 'last_name' in data else None,
                    Employee.nickname == data['nickname'].capitalize() if 'nickname' in data else None
                )
            )
        )

    @staticmethod
    def to_dict(employee: Employee) -> dict:
        data = {
            'id': employee.id,
            'name': employee.name,
            'last_name': employee.last_name,
            'nickname': employee.nickname,
            'main_technology': employee.main_technology,
            'status': employee.status,
            'cv': employee.employee_data.cv,
            'additional_data': employee.employee_data.additional_data
        }
        return data

    @classmethod
    def to_collection_dict(cls, employees: BaseQuery) -> dict:
        return {'employees': {item.id: cls.to_dict(item) for item in employees}}
