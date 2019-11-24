import pytest
import falcon
from falcon import testing
import json
from notifications_microservice.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_get_notifications(client):
    resp = client.simulate_get('/notifications')
    notifications = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert len(notifications) == 5


def test_post_notifications(client):
    resp = client.simulate_request(
        method='POST', path='/notifications', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_CREATED
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/notifications', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "date": "2020:12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/notifications')

    assert resp.status == falcon.HTTP_BAD_REQUEST
    assert resp.headers['Content-Type'] == "application/json"


def test_post_notification(client):
    resp = client.simulate_get('/notifications/0')
    notifications = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert notifications['_Notification__id'] == 0

    resp = client.simulate_get('/notifications/100')
    notification = resp.json

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"


def test_put_notification(client):
    resp = client.simulate_request(
        method='PUT', path='/notifications/0', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/notifications/34', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/notifications/0', json={"subject": "the subject", "content": "a content", "to_mail":"mail@mail.es", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"