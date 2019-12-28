import pytest
import falcon
from falcon import testing
import json
import pymongo
from bson.objectid import ObjectId

from events_microservice.app import api

client = pymongo.MongoClient()
db = client.EventsMicroservice
events_collection = db.Events

@pytest.fixture
def client():
    return testing.TestClient(api)


def test_get_events(client):
    resp = client.simulate_get('/events')
    events = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert len(events) == events_collection.count_documents({})


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
    data = events_collection.find_one()
    resp = client.simulate_get('/events/' + str(data["_id"]))
    event = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_get('/events/aaaaaaaaaaaaaaaaaaaaaaaa')
    event = resp.json

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"


def test_put_event(client):
    data = events_collection.find_one()
    resp = client.simulate_request(
        method='PUT', path='/events/' + str(data["_id"]), json={"title": "one title", "description": "a description"+'a'*23, "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/events/aaaaaaaaaaaaaaaaaaaaaaaa', json={"title": "one title", "description": "a description"+'a'*23, "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"

    data = events_collection.find_one()
    resp = client.simulate_request(
        method='PUT', path='/events/' + str(data["_id"]), json={"title": "one title", "description": "a description", "date": "2020-12-12", "time": "20:50:12"})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"


def test_delete_event(client):
    data = events_collection.find_one()
    resp = client.simulate_request(
        method='DELETE', path='/events/' + str(data["_id"]))

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='DELETE', path='/events/aaaaaaaaaaaaaaaaaaaaaaaa')

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"
