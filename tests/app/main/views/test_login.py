from . import get_cookie_by_name
from app import admin_api_client


def user():
    return {
        "users": {
            "active": True,
            "createdAt": "2015-10-15T08:12:02.693378Z",
            "emailAddress": "test@example.com",
            "failedLoginCount": 0,
            "active": True,
            "id": 1,
            "locked": False,
            "organisationId": 1,
            "passwordChangedAt": "2015-10-15T08:12:02.693378Z",
            "role": "admin",
            "updatedAt": "2015-10-15T08:12:02.693378Z"
        }
    }


def test_should_render_login_page(notify_frontend):
    response = notify_frontend.test_client().get('/admin/login')
    assert response.status_code == 200
    assert "Sign in to GOV.UK Notify" in response.get_data(as_text=True)


def test_should_redirect_to_dashboard_on_login(notify_frontend, mocker):
    mocker.patch('app.admin_api_client.authenticate_user', return_value=user())
    res = notify_frontend.test_client().post(
        "/admin/login",
        data={
            'email_address': 'valid@email.com',
            'password': '1234567890'
        }
    )
    assert res.status_code == 302
    assert res.location == 'http://localhost/admin/dashboard'
    assert 'Secure;' in res.headers['Set-Cookie']
    admin_api_client.authenticate_user.assert_called_once_with("valid@email.com", "1234567890")


def test_should_not_allow_login_if_user_cant_be_found(notify_frontend, mocker):
    mocker.patch('app.admin_api_client.authenticate_user', return_value=None)
    response = notify_frontend.test_client().post(
        "/admin/login",
        data={
            'email_address': 'valid@email.com',
            'password': '1234567890'
        }
    )
    assert response.status_code == 403


def test_should_show_errors_on_form_validation_failure(notify_frontend):
    response = notify_frontend.test_client().post(
        "/admin/login",
        data={
            'email_address': 'invalid-email',
            'password': ''
        }
    )
    assert response.status_code == 400
    assert "There was a problem with your answer to the following questions" in response.get_data(as_text=True)
    assert "Please enter a valid email address" in response.get_data(as_text=True)
    assert "Please enter your password" in response.get_data(as_text=True)


def test_ok_next_url_redirects_on_login(notify_frontend, mocker):
    mocker.patch('app.admin_api_client.authenticate_user', return_value=user())
    res = notify_frontend.test_client().post(
        "/admin/login?next=/admin/3fa",
        data={
            'email_address': 'valid@email.com',
            'password': '1234567890'
        })
    assert res.status_code == 302
    assert res.location == 'http://localhost/admin/3fa'


def test_bad_next_url_takes_user_to_service_page(notify_frontend, mocker):
    mocker.patch('app.admin_api_client.authenticate_user', return_value=user())
    res = notify_frontend.test_client().post(
        "/admin/login?next=http://badness.com",
        data={
            'email_address': 'valid@email.com',
            'password': '1234567890'
        })
    assert res.status_code == 302
    assert res.location == 'http://localhost/admin/dashboard'


def test_should_have_cookie_on_redirect(notify_frontend, mocker):
    mocker.patch('app.admin_api_client.authenticate_user', return_value=user())
    notify_frontend.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
    notify_frontend.config['SESSION_COOKIE_SECURE'] = True
    res = notify_frontend.test_client().post(
        "/admin/login",
        data={
            'email_address': 'valid@email.com',
            'password': '1234567890'
        })
    cookie_value = get_cookie_by_name(res, 'notify_admin_session')
    assert cookie_value['notify_admin_session'] is not None
    assert cookie_value['Secure; HttpOnly; Path'] == '/admin'
    assert cookie_value["Domain"] == "127.0.0.1"


def test_should_redirect_to_login_on_logout(notify_frontend):
    res = notify_frontend.test_client().get('/admin/logout')
    assert res.status_code == 302
    assert res.location == 'http://localhost/admin/login'
