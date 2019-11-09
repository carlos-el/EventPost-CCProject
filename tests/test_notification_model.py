## test_notification_model.py

import sys, os, pytest

sys.path.append(os.path.abspath('./'))

import datetime as dt
from notifications_microservice.models.notification_definition import Notification

id = 1
subject = "test subject"
content = "test content " + 'a'*30 
to_mail = "testmail@testmail.com"
scheduled_time = dt.datetime.now()+dt.timedelta(1)

def test_subject():
    n = Notification(id, subject, content, to_mail, scheduled_time)
    assert n.get_subject() == subject,"Error in subject assignment"

    with pytest.raises(AttributeError):
        _ = Notification(id, None, content, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, "", content, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, 'a'*71, content, to_mail, scheduled_time)

def test_content():
    n = Notification(id, subject, content, to_mail, scheduled_time)
    assert n.get_content() == content,"Error in content assignment"

    with pytest.raises(AttributeError):
        _ = Notification(id, subject, None, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, subject, "", to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, subject, 'a'*701, to_mail, scheduled_time)

def test_to_mail():
    n = Notification(id, subject, content, to_mail, scheduled_time)
    assert n.get_to_mail() == to_mail,"Error in to_mail assignment"

    with pytest.raises(AttributeError):
        _ = Notification(id, subject, content, None, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, subject, content, "notamail@mail", scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(id, subject, content, "notamailmail.com", scheduled_time)

def test_scheduled_time():
    n = Notification(id, subject, content, to_mail, scheduled_time)
    assert n.get_scheduled_time() == scheduled_time,"Error in scheduled_time assignment"

    with pytest.raises(AttributeError):
        _ = Notification(id, subject, content, to_mail, None)
    with pytest.raises(ValueError):
        _ = Notification(id, subject, content, to_mail, dt.datetime.now()-dt.timedelta(1))