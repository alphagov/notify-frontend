import os
from datetime import timedelta

from flask import Flask, request, redirect

from flask._compat import string_types

from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from app.api_client import DataAPIClient
from app.user import User
from config import configs

csrf = CsrfProtect()
login_manager = LoginManager()
data_api_client = DataAPIClient()


def create_app(config_name):

    application = Flask(
        __name__,
        static_folder='static/',
        static_url_path=configs[config_name].STATIC_URL_PATH
    )

    application.config['NOTIFY_ENVIRONMENT'] = config_name
    application.config.from_object(configs[config_name])

    init_app(application)
    csrf.init_app(application)
    login_manager.init_app(application)
    data_api_client.init_app(application)

    from .main import main as main_blueprint
    application.permanent_session_lifetime = timedelta(hours=1)
    application.register_blueprint(main_blueprint, url_prefix='/admin')
    login_manager.login_view = 'main.render_login'

    main_blueprint.config = application.config.copy()

    @application.before_request
    def remove_trailing_slash():
        if request.path != '/' and request.path.endswith('/'):
            return redirect(request.path[:-1], code=301)

    return application


def init_app(app):
    for key, value in app.config.items():
        if key in os.environ:
            app.config[key] = convert_to_boolean(os.environ[key])


@login_manager.user_loader
def load_user(user_id):
    print("user_id")
    return User.load_user()


def convert_to_boolean(value):
    """Turn strings to bools if they look like them

    Truthy things should be True
    >>> for truthy in ['true', 'on', 'yes', '1']:
    ...   assert convert_to_boolean(truthy) == True

    Falsey things should be False
    >>> for falsey in ['false', 'off', 'no', '0']:
    ...   assert convert_to_boolean(falsey) == False

    Other things should be unchanged
    >>> for value in ['falsey', 'other', True, 0]:
    ...   assert convert_to_boolean(value) == value
    """
    if isinstance(value, string_types):
        if value.lower() in ['t', 'true', 'on', 'yes', '1']:
            return True
        elif value.lower() in ['f', 'false', 'off', 'no', '0']:
            return False

    return value


def convert_to_number(value):
    """Turns numeric looking things into floats or ints

    Integery things should be integers
    >>> for inty in ['0', '1', '2', '99999']:
    ...   assert isinstance(convert_to_number(inty), int)

    Floaty things should be floats
    >>> for floaty in ['0.99', '1.1', '1000.0000001']:
    ...   assert isinstance(convert_to_number(floaty), float)

    Other things should be unchanged
    >>> for value in [0, 'other', True, 123]:
    ...   assert convert_to_number(value) == value
    """
    try:
        return float(value) if "." in value else int(value)
    except (TypeError, ValueError):
        return value
