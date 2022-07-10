from flask import url_for


def test_registration_page(client):
    res = client.get(url_for('auth.registration'))
    assert res.status_code == 200


def test_login_page(client):
    res = client.get(url_for('auth.login'))
    assert res.status_code == 200


def test_logout_page(client, auth_login):
    res = client.get(url_for('auth.logout'))
    assert res.status_code == 302


def test_reset_password_request_page(client):
    res = client.get(url_for('auth.reset_password_request'))
    assert res.status_code == 200


def test_reset_password_page(client, token_reset_password):
    res = client.get(url_for('auth.reset_password', token=token_reset_password))
    assert res.status_code == 200
