from app import db
from app.models.dbmodels import Manager
from app.models.forms import RegistrationForm
from flask import redirect, url_for, Response


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
            return redirect(url_for('auth.login'))

    @staticmethod
    def change_password(user: Manager, new_password: str):
        try:
            user.set_password(password=new_password)
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()
