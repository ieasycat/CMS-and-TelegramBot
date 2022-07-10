from flask import url_for
import pytest


@pytest.mark.parametrize('url', ['api.get_employees'])
def test_get_all_employees(client, url, employee, user_headers):
    res = client.get(url_for(url), headers=user_headers)
    assert res.status_code == 200
    assert res.json == {"employees": [{"additional_data": None, "cv": "Testing", "id": 1, "last_name": "Tester",
                                       "main_technology": "Python", "name": "Test",
                                       "nickname": "Python_1", "status": "Free"}]}


@pytest.mark.parametrize('url, id', [
    ('api.get_employee', '1'),
])
def test_get_employee(client, url, id, user_headers, employee):
    res = client.get(url_for(url, employee_id=id), headers=user_headers)
    assert res.status_code == 200
    assert res.json == {'id': 1, 'last_name': 'Tester', 'main_technology': 'Python',
                        'name': 'Test', 'nickname': 'Python_1', 'status': 'Free'}


@pytest.mark.parametrize('url', ['api.add_employee'])
def test_add_employee(client, url, user_headers):
    res = client.post(url_for(url), headers=user_headers, json={
        'name': 'Test1',
        'last_name': 'Apitest',
        'main_technology': 'Python',
        'status': 'Free'
    })
    assert res.status_code == 201
    assert res.json == {'code': 201, 'message': 'OK'}


@pytest.mark.parametrize('url, json', [
    ('api.technology_filter', {'main_technology': 'Python'}),
    ('api.employee_search', {'data': 'Test'})
])
def test_filter_and_search_employees(url, json, client, user_headers, employee):
    res = client.get(url_for(url), headers=user_headers, json=json)
    assert res.status_code == 200
    assert res.json == {'employees': [
            {
                'additional_data': None, 'cv': 'Testing', 'id': 1, 'last_name': 'Tester',
                'main_technology': 'Python', 'name': 'Test',
                'nickname': 'Python_1', 'status': 'Free'
            }
    ]}


@pytest.mark.parametrize('url, id, json', [
    ('api.update_employee', '1', {'name': 'newname'}),
    ('api.update_status', '1', None),
])
def test_update_employee_and_update_status(client, url, id, json, user_headers, employee):
    res = client.put(url_for(url, employee_id=id), headers=user_headers, json=json)
    assert res.status_code == 200
    assert res.json == {'code': 200, 'message': 'OK'}


@pytest.mark.parametrize('url, id', [
    ('api.delete_employee', '1'),
])
def test_delete_employee(client, url, id, user_headers, employee):
    res = client.delete(url_for(url, employee_id=id), headers=user_headers)
    assert res.status_code == 200
    assert res.json == {'code': 200, 'message': 'OK'}
