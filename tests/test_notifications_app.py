import pytest
import falcon
from falcon import testing
import json
import datetime as dt
import pymongo
from bson.objectid import ObjectId

from notifications_microservice.app import api

client = pymongo.MongoClient()
db = client.NotificationsMicroservice
notifications_collection = db.Notifications

@pytest.fixture
def client():
    return testing.TestClient(api)


def test_get_notifications(client):
    resp = client.simulate_get('/notifications')
    notifications = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"
    assert len(notifications) == notifications_collection.count_documents({})


def test_post_notifications(client):
    resp = client.simulate_request(
        method='POST', path='/notifications', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":(dt.datetime.now()+dt.timedelta(1)).isoformat()})

    assert resp.status == falcon.HTTP_CREATED
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/notifications', json={"subject": "the subject", "content": "a content", "to_mail":"mail@mail.es", "scheduled_time":(dt.datetime.now()+dt.timedelta(1)).isoformat()})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='POST', path='/notifications')

    assert resp.status == falcon.HTTP_BAD_REQUEST
    assert resp.headers['Content-Type'] == "application/json"


def test_post_notification(client):
    data = notifications_collection.find_one()
    resp = client.simulate_get('/notifications/' + str(data["_id"]))
    notifications = resp.json

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_get('/notifications/aaaaaaaaaaaaaaaaaaaaaaaa')
    notification = resp.json

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"


def test_put_notification(client):
    data = notifications_collection.find_one()
    resp = client.simulate_request(
        method='PUT', path='/notifications/' + str(data["_id"]), json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":(dt.datetime.now()+dt.timedelta(1)).isoformat()})

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/notifications/aaaaaaaaaaaaaaaaaaaaaaaa', json={"subject": "the subject", "content": "a content"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":(dt.datetime.now()+dt.timedelta(1)).isoformat()})

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='PUT', path='/notifications/' + str(data["_id"]), json={"subject": "the subject", "content": "a content", "to_mail":"mail@mail.es", "scheduled_time":(dt.datetime.now()+dt.timedelta(1)).isoformat()})

    assert resp.status == falcon.HTTP_422
    assert resp.headers['Content-Type'] == "application/json"


def test_delete_event(client):
    data = notifications_collection.find_one()
    resp = client.simulate_request(
        method='DELETE', path='/notifications/' + str(data["_id"]))

    assert resp.status == falcon.HTTP_OK
    assert resp.headers['Content-Type'] == "application/json"

    resp = client.simulate_request(
        method='DELETE', path='/notifications/aaaaaaaaaaaaaaaaaaaaaaaa')

    assert resp.status == falcon.HTTP_NOT_FOUND
    assert resp.headers['Content-Type'] == "application/json"