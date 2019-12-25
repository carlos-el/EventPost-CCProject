# test_event_model.py
import sys
import os

sys.path.append(os.path.abspath('./'))

from events_microservice.models.event import Event
import datetime as dt
import pytest


id = "abcabcabcabcabcabcabcabc"
title = "test title"
description = "test description " + 'a'*60
date = dt.date.today()
time = dt.time(12, 12, 12)
place = "test place"
organizer = "test organizer"
topics = "test topics"


def test_set_id():
    e = Event(title, description, date, time, place, organizer, topics, id)
    assert e.get_id() == id, "Error in Id assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, date, time,
                  place, organizer, topics, 1)
    with pytest.raises(ValueError):
        _ = Event(title, description, date, time, place, organizer, topics, "")


def test_set_organizer():
    _ = Event(title, description, date, time, place, topics=topics, id=id)
    e = Event(title, description, date, time, place, organizer, topics, id)
    assert e.get_organizer() == organizer, "Error in organizer assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, date, time, place, None, topics, id)
    with pytest.raises(ValueError):
        _ = Event(title, description, date, time, place, 'a'*51, topics, id)


def test_set_topics():
    _ = Event(title, description, date, time, place, organizer, id=id)
    e = Event(title, description, date, time, place, organizer, topics, id)
    assert e.get_topics() == topics, "Error in topics assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, date, time, place, organizer, [])
    with pytest.raises(ValueError):
        _ = Event(title, description, date, time, place, organizer, 'a'*51)


def test_set_title():
    e = Event(title, description, date, time, place, organizer, topics)
    assert e.get_title() == title, "Error in title assignment"

    with pytest.raises(AttributeError):
        _ = Event(None, description, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event("", description, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event('a'*61, description, date, time, place, organizer, topics)


def test_set_description():
    e = Event(title, description, date, time, place, organizer, topics)
    assert e.get_description() == description, "Error in description assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, None, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(title, "", date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(title, 'a'*401, date, time, place, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(title, 'a'*19, date, time, place, organizer, topics)


def test_set_date():
    e = Event(title, description, date, time, place, organizer, topics)
    assert e.get_date() == date, "Error in date assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, None, time, place, organizer, topics)


def test_set_time():
    e = Event(title, description, date, time, place, organizer, topics)
    assert e.get_time() == time, "Error in time assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, date, None, place, organizer, topics)


def test_place_type():
    e = Event(title, description, date, time,
              organizer=organizer, topics=topics)
    e = Event(title, description, date, time, place, organizer, topics)
    assert e.get_place() == place, "Error in place assignment"

    with pytest.raises(AttributeError):
        _ = Event(title, description, date, time, None, organizer, topics)
    with pytest.raises(ValueError):
        _ = Event(title, description, date, time, 'a'*101, organizer, topics)
