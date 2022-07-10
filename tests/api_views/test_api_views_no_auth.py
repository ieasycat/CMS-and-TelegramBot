from flask import url_for
import pytest


@pytest.mark.parametrize('url', [
    'api.get_employees',
    'api.technology_filter',
    'api.employee_search',
])
def test_get_and_filter_and_search_employees(client, url):
    res = client.get(url_for(url))
    assert res.status_code == 401
    assert res.data == b'Unauthorized Access'


@pytest.mark.parametrize('url, id', [
    ('api.get_employee', '1'),
])
def test_get_employee(client, url, id):
    res = client.get(url_for(url, employee_id=id))
    assert res.status_code == 401
    assert res.data == b'Unauthorized Access'


@pytest.mark.parametrize('url', ['api.add_employee'])
def test_add_employee(client, url):
    res = client.post(url_for(url))
    assert res.status_code == 401
    assert res.data == b'Unauthorized Access'


@pytest.mark.parametrize('url, id', [
    ('api.update_employee', '1'),
    ('api.update_status', '1'),
])
def test_update_employee_and_update_status(client, url, id):
    res = client.put(url_for(url, employee_id=id))
    assert res.status_code == 401
    assert res.data == b'Unauthorized Access'


@pytest.mark.parametrize('url, id', [
    ('api.delete_employee', '1'),
])
def test_delete_employee(client, url, id):
    res = client.delete(url_for(url, employee_id=id))
    assert res.status_code == 401
    assert res.data == b'Unauthorized Access'
