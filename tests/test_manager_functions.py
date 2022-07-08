from app.controllers.manager_db_controller import ManagerController
from app.models.dbmodels import Manager


def test_add_manager(user):
    assert user.id == 1


def test_get_manager(user):
    manager = ManagerController.get_manager(email='test@playsdev.com')
    assert manager.email == 'test@playsdev.com'


def test_check_manager(user):
    res = ManagerController.check_manager(user, '9215765')
    assert res is None


def test_change_password(user):
    ManagerController.change_password(user, '9215765!')
    manager = Manager.query.get(1)
    assert manager.check_password('9215765!')
