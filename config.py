import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    WTF_CSRF_ENABLED = True
    NOTIFY_HTTP_PROTO = 'http'
    SESSION_COOKIE_NAME = 'notify_admin_session'
    SESSION_COOKIE_PATH = '/admin'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.getenv('NOTIFY_ADMIN_FRONTEND_COOKIE_SECRET')
    NOTIFY_DATA_API_URL = os.getenv('NOTIFY_API_URL', "http://localhost:6001")
    NOTIFY_DATA_API_AUTH_TOKEN = os.getenv('NOTIFY_API_TOKEN', "valid-token")
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB max uploads
    MAX_ROWS_IN_BULK_UPLOAD = 1000
    MAX_MESSAGE_LENGTH_FOR_SMS = 147
    MAX_MESSAGE_LENGTH_FOR_EMAIL = 1000
    ALLOWED_EXTENSIONS = set(['csv'])

    STATIC_URL_PATH = '/admin/static'
    ASSET_PATH = STATIC_URL_PATH + '/'
    BASE_TEMPLATE_DATA = {
        'header_class': 'with-proposition',
        'asset_path': ASSET_PATH
    }


class Test(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "not-so-secret"


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = "not-so-secret"


class Live(Config):
    DEBUG = False
    NOTIFY_HTTP_PROTO = 'https'


class Staging(Config):
    DEBUG = False


configs = {
    'development': Development,
    'preview': Live,
    'staging': Staging,
    'production': Live,
    'test': Test,
}
