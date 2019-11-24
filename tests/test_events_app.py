import pytest
import falcon
from falcon import testing
import json
from events_microservice.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_get_events(client):
    resp = client.simulate_get('/events')
    events = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert len(events) == 5


def test_post_events(client):
    resp = client.simulate_request(
        method='POST', path='/events', json={"title": "one title", "description": "a description"+'a'*23, "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_CREATED
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/events', json={"title": "one title", "description": "a description"+'a'*23, "date": "2020:12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/events')

    assert resp.status == falcon.HTTP_BAD_REQUEST
    assert resp.headers['Content-Type'] == "application/json"


def test_post_event(client):
    resp = client.simulate_get('/events/0')
    event = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert event['_Event__id'] == 0

    resp = client.simulate_get('/events/100')
    event = resp.json

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"


def test_put_event(client):
    resp = client.simulate_request(
        method='PUT', path='/events/0', json={"title": "one title", "description": "a description"+'a'*23, "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/events/34', json={"title": "one title", "description": "a description"+'a'*23, "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/events/0', json={"title": "one title", "description": "a description", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"
