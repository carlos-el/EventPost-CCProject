import sys
import os

sys.path.append(os.path.abspath('./'))

from events_microservice.models.event import Event
from events_microservice.models.event_dator import MongoEventDator
import datetime as dt
import pytest

import pymongo
from bson.objectid import ObjectId
import json

ev0 = Event("test title", "test description " + 'a'*60, dt.date.today(), dt.time(10, 10, 10), "test place",
           organizer="test organizer", topics="test topics", id=None)
ev1 = Event("test title1", "test description1 " + 'a'*60, dt.date.today(), dt.time(11, 11, 11), "test place1",
           organizer="test organizer1", topics="test topics1", id=None)
ev2 = Event("test title2", "test description2 " + 'a'*60, dt.date.today(), dt.time(12, 12, 12), "test place2",
           organizer="test organizer2", topics="test topics2", id=None)

ev_t = Event("test titlet", "test descriptiont " + 'a'*60, dt.date.today(), dt.time(12, 12, 12), "test placet",
           organizer="test organizert", topics="test topicst", id=None)


client = pymongo.MongoClient()
db = client.EventsMicroservice
events_collection = db.Events
ids = []

@pytest.fixture(autouse=True, scope='module')
def setup_teardown():
    # Setup section
    ids.append(str(events_collection.insert_one(ev0.to_json()).inserted_id))
    ids.append(str(events_collection.insert_one(ev1.to_json()).inserted_id))
    ids.append(str(events_collection.insert_one(ev2.to_json()).inserted_id))

    yield
    # Teardown section
    for id in ids:
        events_collection.delete_one({"_id": ObjectId(id)})

def test_get_events():
    ed = MongoEventDator()
    events = ed.get_all()

    assert len(events) == events_collection.count_documents({}), "Error in event_mongo_dator, get_all()"
    assert isinstance(
        events[0], Event), "Error in event_mongo_dator, get_all()"


def test_get_by_id():
    ed = MongoEventDator()
    e = ed.get_by_id(ids[0])

    assert e.get_id() == ids[0], "Error in event_mongo_dator, get_by_id()"
    with pytest.raises(ValueError):
        _ = ed.get_by_id("aaaaaaaaaaaaaaaaaaaaaaaa")
    with pytest.raises(AttributeError):
        _ = ed.get_by_id(1)


def test_save():
    ed = MongoEventDator()
    previous_size = events_collection.count_documents({})
    data = events_collection.find_one({"_id": ObjectId(ids[1])})
    ev = ed.db_dict_to_event(data)

    ev_test = ed.save(ev)

    assert ed.get_by_id(ids[1]).get_id() == ev_test.get_id(), "Error in event_mongo_dator, save()"
    assert len(ed.get_all()) == previous_size, "Error in event_mongo_dator, save()"

    ev_test = ed.save(ev_t)

    assert len(ed.get_all()) == previous_size + 1, "Error in event_mongo_dator, save()"

def test_delete_by_id():
    ed = MongoEventDator()
    previous_size = events_collection.count_documents({})
    data = events_collection.find_one({"_id": ObjectId(ids[2])})
    e = ed.db_dict_to_event(data)
    e2 = ed.delete_by_id(e.get_id())

    assert len(ed.get_all()) == previous_size - 1, "Error in event_mongo_dator, delete_by_id()"
    assert e.get_id() == e2.get_id(), "Error in event_mongo_dator, delete_by_id()"
    assert ed.delete_by_id("aaaaaaaaaaaaaaaaaaaaaaaa") == None, "Error in event_mongo_dator, delete_by_id()"
    with pytest.raises(AttributeError):
        _ = ed.delete_by_id(1)
