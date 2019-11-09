## test_event_model.py
import sys, os, pytest

sys.path.append(os.path.abspath('./'))

import datetime as dt
from events_microservice.models.event_definition import Event

id = 1
title = "test title"
description = "test description " + 'a'*60
date = dt.date.today()
time = dt.time(12,12,12)
place = "test place"
organizer = "test organizer"
topics = "test topics"

def test_set_organizer():
    _ = Event(id, title, description, date, time, place, topics=topics)
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_organizer() == organizer,"Error in organizer assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, description, date, time, place, None, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, description, date, time, place, 'a'*51, topics)

def test_set_topics():
    _ = Event(id, title, description, date, time, place, organizer)
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_topics() == topics,"Error in topics assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, description, date, time, place, organizer, [])
    with pytest.raises(ValueError):
        _ = Event(id, title, description, date, time, place, organizer, 'a'*51)

def test_set_title():
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_title() == title,"Error in title assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, None, description, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, "", description, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, 'a'*61, description, date, time, place, organizer, topics)

def test_set_description():
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_description() == description,"Error in description assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, None, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, "", date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, 'a'*401, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, 'a'*59, date, time, place, organizer, topics)

def test_set_date():
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_date() == date,"Error in date assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, description, None, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, description, dt.date(2000,10,10), time, place, organizer, topics)

def test_set_time():
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_time() == time,"Error in time assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, description, date, None, place, organizer, topics)

def test_place_type():
    e = Event(id, title, description, date, time, organizer = organizer, topics = topics)
    e = Event(id, title, description, date, time, place, organizer, topics)
    assert e.get_place() == place,"Error in place assignment"

    with pytest.raises(AttributeError):
        _ = Event(id, title, description, date, time, None, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(id, title, description, date, time, 'a'*101, organizer, topics)
