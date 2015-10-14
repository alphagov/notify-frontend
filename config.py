import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_NAME = 'notify_admin_session'
    SESSION_COOKIE_PATH = '/admin'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.getenv('NOTIFY_ADMIN_FRONTEND_COOKIE_SECRET')

    STATIC_URL_PATH = '/admin/static'
    ASSET_PATH = STATIC_URL_PATH + '/'
    BASE_TEMPLATE_DATA = {
        'header_class': 'with-proposition',
        'asset_path': ASSET_PATH
    }


class Test(Config):
    DEBUG = True


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class Live(Config):
    DEBUG = False


class Staging(Config):
    DEBUG = False


configs = {
    'development': Development,
    'preview': Live,
    'staging': Staging,
    'production': Live,
    'test': Test,
}
