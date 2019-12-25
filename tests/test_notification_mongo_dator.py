import sys
import os

sys.path.append(os.path.abspath('./'))

from notifications_microservice.models.notification import Notification
from notifications_microservice.models.notification_dator import MongoNotificationDator
import datetime as dt
import pytest

import pymongo
from bson.objectid import ObjectId
import json

nt0 = Notification("test subject", "test content"+'a'*30, "testmail@testmail.com", dt.datetime.now()+dt.timedelta(1))
nt1 = Notification("test subject1", "test content1"+'a'*30, "testmail@testmail.com", dt.datetime.now()+dt.timedelta(1))
nt2 = Notification("test subject2", "test content2"+'a'*30, "testmail@testmail.com", dt.datetime.now()+dt.timedelta(1))
nt_t = Notification("test subjectt", "test contentt"+'a'*30, "testmail@testmail.com", dt.datetime.now()+dt.timedelta(1))

client = pymongo.MongoClient()
db = client.NotificationsMicroservice
notifications_collection = db.Notifications
ids = []

@pytest.fixture(autouse=True, scope='module')
def setup_teardown():
    # Setup section
    ids.append(str(notifications_collection.insert_one(nt0.to_json()).inserted_id))
    ids.append(str(notifications_collection.insert_one(nt1.to_json()).inserted_id))
    ids.append(str(notifications_collection.insert_one(nt2.to_json()).inserted_id))

    yield
    # Teardown section
    for id in ids:
        notifications_collection.delete_one({"_id": ObjectId(id)})

def test_get_notifications():
    nd = MongoNotificationDator()
    notifications = nd.get_all()

    assert len(notifications) == notifications_collection.count_documents({}), "Error in notification_mongo_dator, get_all()"
    assert isinstance(
        notifications[0], Notification), "Error in notification_mongo_dator, get_all()"


def test_get_by_id():
    nd = MongoNotificationDator()
    n = nd.get_by_id(ids[0])

    assert n.get_id() == ids[0], "Error in notification_mongo_dator, get_by_id()"
    with pytest.raises(ValueError):
        _ = nd.get_by_id("aaaaaaaaaaaaaaaaaaaaaaaa")
    with pytest.raises(AttributeError):
        _ = nd.get_by_id(1)


def test_save():
    nd = MongoNotificationDator()
    previous_size = notifications_collection.count_documents({})
    data = notifications_collection.find_one({"_id": ObjectId(ids[1])})
    nt = nd.db_dict_to_notification(data)

    nt_test = nd.save(nt)

    assert nd.get_by_id(ids[1]).get_id() == nt_test.get_id(), "Error in notification_mongo_dator, save()"
    assert len(nd.get_all()) == previous_size, "Error in notification_mongo_dator, save()"

    nt_test = nd.save(nt_t)

    assert len(nd.get_all()) == previous_size + 1, "Error in notification_mongo_dator, save()"


def test_delete_by_id():
    nd = MongoNotificationDator()
    previous_size = notifications_collection.count_documents({})
    data = notifications_collection.find_one({"_id": ObjectId(ids[2])})
    n = nd.db_dict_to_notification(data)
    n2 = nd.delete_by_id(n.get_id())

    assert len(nd.get_all()) == previous_size - 1, "Error in notification_mongo_dator, delete_by_id()"
    assert n.get_id() == n2.get_id(), "Error in notification_mongo_dator, delete_by_id()"
    assert nd.delete_by_id("aaaaaaaaaaaaaaaaaaaaaaaa") == None, "Error in notification_mongo_dator, delete_by_id()"
    with pytest.raises(AttributeError):
        _ = nd.delete_by_id(1)
