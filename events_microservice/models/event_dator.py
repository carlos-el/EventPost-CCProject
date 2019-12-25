# event_dator.py file, EventDator is currently a mock for giving data.

import pymongo
from bson.objectid import ObjectId
import json
import datetime as dt

from events_microservice.utils.singleton import Singleton
from events_microservice.models.event import Event


class MongoEventDator(metaclass=Singleton):
    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client.EventsMicroservice
        self.__events = db.Events

    def db_dict_to_event(self, data):
        # Changes key name from '_id' to 'id' and cast key value from ObjectId to str
        data["id"] = str(data.pop("_id"))
        date = data['date'].split('-')
        time = data['time'].split(':')
        return Event(data["title"], data["description"], 
                dt.date(int(date[0]), int(date[1]), int(date[2])), 
                dt.time(int(time[0]), int(time[1]), int(time[2])), 
                data["place"], data["organizer"], data["topics"], data["id"])

    def get_all(self): 
        evs = []
        for data in self.__events.find():
            evs.append(self.db_dict_to_event(data))

        return evs

    def get_by_id(self, id):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")

        data = self.__events.find_one({"_id": ObjectId(id)})
        if data is None:
            raise ValueError("Could not find specified id.")
        else:
            return self.db_dict_to_event(data)

    def save(self, event):
        ev_json = event.to_json()
        ev_json.pop("id")
        data = self.__events.find_one_and_update({"_id": ObjectId(event.get_id())}, {'$set': ev_json}, 
                                                return_document=pymongo.ReturnDocument.AFTER)

        if data is None:
            result = self.__events.insert_one(ev_json)
            data = self.__events.find_one({"_id": ObjectId(result.inserted_id)})
            return self.db_dict_to_event(data)
        else:
            return self.db_dict_to_event(data)


    def delete_by_id(self, id):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")
            
        data = self.__events.find_one_and_delete({"_id": ObjectId(id)})
        if data is None:
            return None
        else:
            return self.db_dict_to_event(data)

    

class EventDatorMock(metaclass=Singleton):  
    def __init__(self):
        self.__data = {
            "aaaaaaaaaaaaaaaaaaaaaaa0": Event("Evento 1, un titulo", "Breve (o no tanto) descripcion del evento 1. Relleno de contenido en este evento", dt.date(2020, 1, 1), dt.time(20, 50, 10), "Plaza Mayor 1", "Nadie real1.", "Tema libre1", "aaaaaaaaaaaaaaaaaaaaaaa0"),
            "aaaaaaaaaaaaaaaaaaaaaaa1": Event("Evento 1, un titulo", "Breve (o no tanto) descripcion del evento 1. Relleno de contenido en este evento", dt.date(2020, 1, 1), dt.time(20, 50, 10), "Plaza Mayor 1", "Nadie real1.", "Tema libre1", "aaaaaaaaaaaaaaaaaaaaaaa1"),
            "aaaaaaaaaaaaaaaaaaaaaaa2": Event("Evento 2, dos titulo", "Breve (o no tanto) descripcion del evento dos. Relleno de contenido en este evento", dt.date(2020, 2, 2), dt.time(20, 50, 20), "Plaza Mayor 2", "Nadie real2.", "Tema libre2", "aaaaaaaaaaaaaaaaaaaaaaa2"),
            "aaaaaaaaaaaaaaaaaaaaaaa3": Event("Evento 3, tres titulo", "Breve (o no tanto) descripcion del evento 3. Relleno de contenido en este evento", dt.date(2020, 3, 3), dt.time(20, 50, 30), "Plaza Mayor 3", "Nadie real3.", "Tema libre3", "aaaaaaaaaaaaaaaaaaaaaaa3"),
            "aaaaaaaaaaaaaaaaaaaaaaa4": Event("Evento 4,  cuatro titulo", "Breve (o no tanto) descripcion del evento cuatro. Relleno de contenido en este evento", dt.date(2020, 4, 4), dt.time(20, 50, 40), "Plaza Mayor 4", "Nadie real4.", "Tema libre4", "aaaaaaaaaaaaaaaaaaaaaaa4"),
        }

    def get_all(self): 
        return list(self.__data.values())

    def get_by_id(self, id): 
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")
        if id not in self.__data:
            raise ValueError("Could not find specified id.")
        else:
            return self.__data[id]

    def save(self, event):
        # check if that id already exist
        if event.get_id() in self.__data:
            # if it does
            self.__data[event.get_id()] = event

            return event
        else:
            # if it doesn't
            new_id = list(self.__data.keys())[len(self.__data)-1] 
            last_number = str(int(new_id.split("a")[-1]) + 1)
            new_id = new_id[:-len(last_number)]
            new_id = new_id + last_number
            
            new = Event(event.get_title(), event.get_description(), event.get_date(), event.get_time(
            ), event.get_place(), event.get_organizer(), event.get_topics(), new_id)
            self.__data[new_id] = new

            return new

    def delete_by_id(self, id):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")
        if id in self.__data:
            return self.__data.pop(id, None)

