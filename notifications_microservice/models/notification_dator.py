# notification_dator.py file, NotificationDator is currently a mock for giving data.

import pymongo
from bson.objectid import ObjectId
import json
import datetime as dt

from notifications_microservice.utils.singleton import Singleton
from notifications_microservice.models.notification import Notification


class MongoNotificationDator(metaclass=Singleton):
    def __init__(self):
        client = pymongo.MongoClient()
        db = client.NotificationsMicroservice
        self.__notifications = db.Notifications

    def db_dict_to_notification(self, data):
        # Changes key name from '_id' to 'id' and cast key value from ObjectId to str
        data["id"] = str(data.pop("_id"))
        tmp = data["scheduled_time"].split('T')
        tmp2 = tmp[1].split('.')
        date = tmp[0].split('-')
        time = tmp2[0].split(':')
        return Notification(data['subject'], data['content'], data['to_mail'], 
                            dt.datetime(int(date[0]), int(date[1]), int(date[2]), 
                            int(time[0]), int(time[1]), int(time[2])), data["id"])

    def get_all(self): 
        nts = []
        for data in self.__notifications.find():
            nts.append(self.db_dict_to_notification(data))

        return nts

    def get_by_id(self, id):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")

        data = self.__notifications.find_one({"_id": ObjectId(id)})
        if data is None:
            raise ValueError("Could not find specified id.")
        else:
            return self.db_dict_to_notification(data)

    def save(self, event):
        nt_json = event.to_json()
        nt_json.pop("id")
        data = self.__notifications.find_one_and_update({"_id": ObjectId(event.get_id())}, {'$set': nt_json}, 
                                                return_document=pymongo.ReturnDocument.AFTER)

        if data is None:
            result = self.__notifications.insert_one(nt_json)
            data = self.__notifications.find_one({"_id": ObjectId(result.inserted_id)})
            return self.db_dict_to_notification(data)
        else:
            return self.db_dict_to_notification(data)


    def delete_by_id(self, id):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")
            
        data = self.__notifications.find_one_and_delete({"_id": ObjectId(id)})
        if data is None:
            return None
        else:
            return self.db_dict_to_notification(data)


class NotificationDatorMock(metaclass=Singleton): 
    def __init__(self):
        self.__data = {
            "aaaaaaaaaaaaaaaaaaaaaaa0":  Notification("test subject 0", "test content 0"+'a'*30, "testmail0@testmail.com", dt.datetime.now()+dt.timedelta(1), "aaaaaaaaaaaaaaaaaaaaaaa0"),
            "aaaaaaaaaaaaaaaaaaaaaaa1":  Notification("test subject 1", "test content 1"+'a'*30, "testmail1@testmail.com", dt.datetime.now()+dt.timedelta(1), "aaaaaaaaaaaaaaaaaaaaaaa1"),
            "aaaaaaaaaaaaaaaaaaaaaaa2":  Notification("test subject 2", "test content 2"+'a'*30, "testmail2@testmail.com", dt.datetime.now()+dt.timedelta(1), "aaaaaaaaaaaaaaaaaaaaaaa2"),
            "aaaaaaaaaaaaaaaaaaaaaaa3":  Notification("test subject 3", "test content 3"+'a'*30, "testmail3@testmail.com", dt.datetime.now()+dt.timedelta(1), "aaaaaaaaaaaaaaaaaaaaaaa3"),
            "aaaaaaaaaaaaaaaaaaaaaaa4":  Notification("test subject 4", "test content 4"+'a'*30, "testmail4@testmail.com", dt.datetime.now()+dt.timedelta(1), "aaaaaaaaaaaaaaaaaaaaaaa4"),
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
            new_id = list(self.__data.keys())[len(self.__data)-1] 
            last_number = str(int(new_id.split("a")[-1]) + 1)
            new_id = new_id[:-len(last_number)]
            new_id = new_id + last_number

            new =  Notification(notification.get_subject(), notification.get_content(), notification.get_to_mail(), notification.get_scheduled_time(), new_id)
            self.__data[new.get_id()] = new

            return new

    def delete_by_id(self, id):
        if id in self.__data:
            return self.__data.pop(id, None)