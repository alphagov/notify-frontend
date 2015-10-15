import pytest
import mock
from app import create_app
from config import configs


@pytest.fixture(scope='session')
def notify_frontend(request):
    print("setting up notify frontend")
    app = create_app('test')
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def notify_config(notify_frontend):
    notify_frontend.config['NOTIFY_API_ENVIRONMENT'] = 'test'
    notify_frontend.config.from_object(configs['test'])


@pytest.fixture
def os_environ(request):
    env_patch = mock.patch('os.environ', {})
    request.addfinalizer(env_patch.stop)

    return env_patch.start()
