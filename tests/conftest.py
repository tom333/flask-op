import pytest

from flask_op.flask_op import create_app


@pytest.fixture
def app():
    app = create_app('config.py')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()