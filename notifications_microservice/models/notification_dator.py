# notification_dator.py file, NotificationDator is currently a mock for giving data.

from lib.singleton import Singleton
from notifications_microservice.models.notification import Notification
import datetime as dt


class NotificationDatorMock(metaclass=Singleton): 
    def __init__(self):
        self.__data = {
            0:  Notification("test subject 0", "test content 0"+'a'*30, "testmail0@testmail.com", dt.datetime.now()+dt.timedelta(1), 0),
            1:  Notification("test subject 1", "test content 1"+'a'*30, "testmail1@testmail.com", dt.datetime.now()+dt.timedelta(1), 1),
            2:  Notification("test subject 2", "test content 2"+'a'*30, "testmail2@testmail.com", dt.datetime.now()+dt.timedelta(1), 2),
            3:  Notification("test subject 3", "test content 3"+'a'*30, "testmail3@testmail.com", dt.datetime.now()+dt.timedelta(1), 3),
            4:  Notification("test subject 4", "test content 4"+'a'*30, "testmail4@testmail.com", dt.datetime.now()+dt.timedelta(1), 4),
        }

    def get_all(self):  
        return list(self.__data.values())

    def get_by_id(self, id):  
        if id not in self.__data:
            raise ValueError("Could not find specified id.")
        else:
            return self.__data[id]

    def save(self, notification):
        # check if that id already exist
        if notification.get_id() in self.__data:
            # if it does
            self.__data[notification.get_id()] = notification

            return notification
        else:
            # if it doesn't
            new_id = max(self.__data.keys()) + 1

            new =  Notification(notification.get_subject(), notification.get_content(), notification.get_to_mail(), notification.get_scheduled_time(), new_id)
            self.__data[new.get_id()] = new

            return new

    def delete_by_id(self, id):
        if id in self.__data:
            return self.__data.pop(id, None)