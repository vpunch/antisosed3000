from http import HTTPStatus

from flask import g
import pytest

from .utils import get_tg_cmd
from entity import Entities, Districts


@pytest.fixture(scope='module')
def distrs():
    districts = Districts()
    yield districts.get()
    del Entities._cache[districts.id]


def test_distr_cache(app, distrs):
    districts = Districts()
    res = districts.get()

    assert districts.id in Entities._cache
    assert Entities._cache[districts.id] is res


def test_distr_reqq():
    # is OK
    pass


@pytest.fixture(scope='session')
def distrs_req(tg_client, client): 
    with client:
        response = tg_client(get_tg_cmd('ep'))
        return g.messages


def hosps_req(distrs_req, ):


def specials_req(hosps_req):
    


def test_distrs_list(app, distrs_req):
    assert len(distrs_req) == 1

    text = distrs_req[0].text
    # Может приводить к ошибке
    assert len(text.split('\n\n')) == app.config['PAGE_SIZE'] + 1


def test_distrs_forward(distrs_req):
    pass
    #distrs_req[0]


def test_start(client, tg_client):
    with client:
        response = tg_client(get_tg_cmd('start'))

        assert len(g.messages) == 2

    assert response.status_code == HTTPStatus.OK


def test_special_subscr(db, specials_req):
    pass


def test_service():
    :ass
