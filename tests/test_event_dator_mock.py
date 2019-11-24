# test_event_dator_mock.py
import sys
import os

sys.path.append(os.path.abspath('./'))

from events_microservice.models.event import Event
from events_microservice.models.event_dator import EventDatorMock
import datetime as dt
import pytest

ev = Event("test title", "test description " + 'a'*60, dt.date.today(), dt.time(12, 12, 12), "test place",
           organizer="test organizer", topics="test topics", id=None)


def test_get_events():
    ed = EventDatorMock()
    events = ed.get_all()

    assert len(events) == 5, "Error in event_dator_ mock, get_all()"
    assert isinstance(
        events[0], Event), "Error in event_dator_ mock, get_all()"


def test_get_by_id():
    ed = EventDatorMock()
    e = ed.get_by_id(1)

    assert e.get_id() == 1, "Error in event_dator_ mock, get_by_id()"
    with pytest.raises(ValueError):
        _ = ed.get_by_id(100)
    with pytest.raises(AttributeError):
        _ = ed.get_by_id("1")


def test_save():
    ed = EventDatorMock()
    ev2 = ed.save(ev)
    events = ed.get_all()

    assert len(events) == 6, "Error in event_dator_ mock, save()"
    assert ed.get_by_id(5) == ev2, "Error in event_dator_ mock, save()"


def test_delete_by_id():
    ed = EventDatorMock()
    e = ed.get_by_id(5)
    e2 = ed.delete_by_id(e.get_id())

    assert len(ed.get_all()) == 5, "Error in event_dator_ mock, delete_by_id()"
    assert e == e2, "Error in event_dator_ mock, delete_by_id()"
    assert ed.delete_by_id(-1) == None, "Error in event_dator_ mock, delete_by_id()"
    with pytest.raises(AttributeError):
        _ = ed.delete_by_id("1")

