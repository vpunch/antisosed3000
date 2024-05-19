from typing import Final

from pathlib import Path
import pytest
from flask import Flask

from app import create_app, create_tables
from entity import Entities, Districts


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    db_path = Path(app.instance_path) / app.config['DB_NAME']
    db_path.unlink(True)
    create_tables(app)

    yield app


#def db


@pytest.fixture(scope='session')
def client(app: Flask):
    return app.test_client()


@pytest.fixture(scope='session')
def tg_client(app, client):
    def send_request(message: dict):
        return client.post('/' + app.config['TG_TOKEN'], json=message)

    return send_request
