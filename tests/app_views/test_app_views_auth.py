from flask import url_for
import pytest


@pytest.mark.parametrize('url', [
    'main.index',
    'employee.add_user',
])
def test_main_and_add_page_authorization(client, url, auth_login):
    res = client.get(url_for(url))
    assert res.status_code == 200


def test_filter_page_authorization(client, auth_login):
    res = client.post(url_for('employee.technology_filter', main_technology='Python'))
    assert res.status_code == 200


def test_search_page_authorization(client, auth_login):
    res = client.post(url_for('employee.employee_search', data='Anton'))
    assert res.status_code == 200


def test_update_user_page_authorization(client, auth_login, employee):
    res = client.get(url_for('employee.update_user', employee_id=employee.id))
    assert res.status_code == 200
