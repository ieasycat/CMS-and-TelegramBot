from flask import url_for
import pytest


@pytest.mark.parametrize('url', [
    'main.index',
    'employee.add_user',
])
def test_page_no_authorization_get(client, url):
    res = client.get(url_for(url))
    assert res.status_code == 302


@pytest.mark.parametrize('url', [
    'main.index',
    'employee.add_user',
])
def test_page_no_authorization_post(client, url):
    res = client.post(url_for(url))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.technology_filter', 'Python')
])
def test_page_no_authorization_filter_get(url, data, client):
    res = client.get(url_for(url, main_technology=data))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.technology_filter', 'Python')
])
def test_page_no_authorization_filter_post(url, data, client):
    res = client.post(url_for(url, main_technology=data))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.employee_search', 'Anton')
])
def test_page_no_authorization_search_get(url, data, client):
    res = client.get(url_for(url, data=data))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.employee_search', 'Anton')
])
def test_page_no_authorization_search_post(url, data, client):
    res = client.post(url_for(url, data=data))
    assert res.status_code == 302


@pytest.mark.parametrize('url, id', [
    ('employee.update_user', '1')
])
def test_page_no_authorization_with_id_get(url, id, client):
    res = client.get(url_for(url, employee_id=id))
    assert res.status_code == 302


@pytest.mark.parametrize('url, id', [
    ('employee.update_user', '1'),
    ('employee.update_status', '1'),
    ('employee.delete_user', '1')
])
def test_page_no_authorization_with_id_post(url, id, client):
    res = client.post(url_for(url, employee_id=id))
    assert res.status_code == 302
