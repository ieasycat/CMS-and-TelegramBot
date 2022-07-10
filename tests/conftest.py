import pytest
from flask import url_for
from app import create_app, db
from app.controllers.manager_db_controller import ManagerController
from app.controllers.employee_db_controller import EmployeeController
from app.models.dbmodels import Manager, Employee
from app.models.forms import RegistrationForm, AddEmployeeForm


# pytest_plugins = []


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            })

    with app.app_context(), app.test_request_context():
        db.expire_on_commit = False
        db.create_all()
        yield app
        db.session.commit()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    test_form = RegistrationForm(email='test@playsdev.com', password='9215765')
    ManagerController.add_manager(test_form)
    user = db.session.query(Manager).filter_by(email='test@playsdev.com').first()
    return user


@pytest.fixture
def auth_login(user, client):
    return client.post(url_for('auth.login'), data={
        'email': user.email,
        'password': '9215765'
    })


@pytest.fixture
def employee(app):
    test_form = AddEmployeeForm(
        name='Test',
        last_name='Tester',
        main_technology='Python',
        status='Free',
        cv='Testing'
    )
    EmployeeController.add_employee(test_form)
    employee = db.session.query(Employee).filter_by(name='Test').first()
    return employee


@pytest.fixture
def token_reset_password(user):
    return user.get_reset_password_token()


@pytest.fixture
def user_headers(user):
    headers = {
        'Authorization': f'Bearer {user.get_token()}'
    }

    return headers
