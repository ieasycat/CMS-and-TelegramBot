from app import db
from app.controllers.manager_db_controller import ManagerController
from app.models.dbmodels import Manager
from app.models.forms import RegistrationForm


def test_add_manager(app):
    test_form = RegistrationForm(email='test1@test.com', password='1234567890Q')
    ManagerController.add_manager(test_form)
    user = db.session.query(Manager).filter_by(email='test1@test.com').first()
    assert user.email == 'test1@test.com'


def test_get_manager(user):
    manager = ManagerController.get_manager(email=user.email)
    assert manager.email == 'test@test.com'


def test_check_manager(user):
    res = ManagerController.check_manager(user, '1234567890Q')
    assert res is None


def test_change_password(user):
    ManagerController.change_password(user, '1234567890Q!')
    assert user.check_password('1234567890Q!')
