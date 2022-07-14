from flask import url_for
import pytest


@pytest.mark.parametrize('url', [
    'main.index',
    'employee.add_user',
])
def test_main_and_add_page_no_authorization(client, url):
    res = client.get(url_for(url))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.technology_filter', {'technology': 'Python', 'programmer_level': 'Middle'})
])
def test_filter_page_no_authorization(url, data, client):
    res = client.post(url_for(url, main_technology=data['technology'], programmer_level=data['programmer_level']))
    assert res.status_code == 302


@pytest.mark.parametrize('url, data', [
    ('employee.employee_search', 'Anton')
])
def test_search_page_no_authorization(url, data, client):
    res = client.post(url_for(url, data=data))
    assert res.status_code == 302


@pytest.mark.parametrize('url, id', [
    ('employee.update_user', '1'),
    ('employee.update_status', '1'),
    ('employee.delete_user', '1')
])
def test_update_user_and_status_and_delete_user_page_no_authorization(url, id, client):
    res = client.post(url_for(url, employee_id=id))
    assert res.status_code == 302
