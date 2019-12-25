## test_notification_model.py

import sys, os, pytest

sys.path.append(os.path.abspath('./'))

import datetime as dt
from notifications_microservice.models.notification import Notification

id = "abcabcabcabcabcabcabcabc"
subject = "test subject"
content = "test content " + 'a'*30 
to_mail = "testmail@testmail.com"
scheduled_time = dt.datetime.now()+dt.timedelta(1)

def test_id():
    n = Notification(subject, content, to_mail, scheduled_time, id)
    assert n.get_id() == id, "Error in Id assignment"

    with pytest.raises(AttributeError):
        _ = Notification(subject, content, to_mail, scheduled_time, 1)
    with pytest.raises(ValueError):
        _ =  Notification(subject, content, to_mail, scheduled_time, "")



def test_subject():
    n = Notification(subject, content, to_mail, scheduled_time)
    assert n.get_subject() == subject,"Error in subject assignment"

    with pytest.raises(AttributeError):
        _ = Notification(None, content, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification("", content, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification('a'*71, content, to_mail, scheduled_time)

def test_content():
    n = Notification(subject, content, to_mail, scheduled_time)
    assert n.get_content() == content,"Error in content assignment"

    with pytest.raises(AttributeError):
        _ = Notification(subject, None, to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(subject, "", to_mail, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(subject, 'a'*701, to_mail, scheduled_time)

def test_to_mail():
    n = Notification(subject, content, to_mail, scheduled_time)
    assert n.get_to_mail() == to_mail,"Error in to_mail assignment"

    with pytest.raises(AttributeError):
        _ = Notification(subject, content, None, scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(subject, content, "notamail@mail", scheduled_time)
    with pytest.raises(ValueError):
        _ = Notification(subject, content, "notamailmail.com", scheduled_time)

def test_scheduled_time():
    n = Notification(subject, content, to_mail, scheduled_time)
    assert n.get_scheduled_time() == scheduled_time,"Error in scheduled_time assignment"

    with pytest.raises(AttributeError):
        _ = Notification(subject, content, to_mail, None)
    # with pytest.raises(ValueError):
    #     _ = Notification(subject, content, to_mail, dt.datetime.now()-dt.timedelta(1))