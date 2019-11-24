# test_notification_dator_mock.py
import sys
import os

sys.path.append(os.path.abspath('./'))

from notifications_microservice.models.notification import Notification
from notifications_microservice.models.notification_dator import NotificationDatorMock
import datetime as dt
import pytest

no = Notification("test subject", "test content"+'a'*30, "testmail@testmail.com", dt.datetime.now()+dt.timedelta(1))


def test_get_notificationss():
    nd = NotificationDatorMock()
    notifications = nd.get_all()

    assert len(notifications) == 5, "Error in notification_dator mock, get_all()"
    assert isinstance(
        notifications[0], Notification), "Error in notification_dator mock, get_all()"


def test_get_by_id():
    nd = NotificationDatorMock()
    e = nd.get_by_id(1)

    assert e.get_id() == 1, "Error in notification_dator mock, get_by_id()"
    with pytest.raises(ValueError):
        _ = nd.get_by_id(100)


def test_save():
    nd = NotificationDatorMock()
    no2 = nd.save(no)
    notifications = nd.get_all()

    assert len(notifications) == 6, "Error in notification_dator mock, save()"
    assert nd.get_by_id(5) == no2, "Error in notification_dator mock, save()"


def test_delete_by_id():
    nd = NotificationDatorMock()
    n = nd.get_by_id(5)
    n2 = nd.delete_by_id(n.get_id())

    assert len(nd.get_all()) == 5, "Error in notification_dator mock, delete_by_id()"
    assert n == n2, "Error in notification_dator mock, delete_by_id()"
    assert nd.delete_by_id(-1) == None, "Error in notification_dator mock, delete_by_id()"

