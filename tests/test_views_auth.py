from flask import url_for
import pytest


@pytest.mark.parametrize('url', [
    'main.index',
    'employee.add_user',
])
def test_page_authorization_get(client, url, auth_login):
    res = client.get(url_for(url))
    assert res.status_code == 200
