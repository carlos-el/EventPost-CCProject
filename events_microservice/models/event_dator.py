# event_dator.py file, EventDator is currently a mock for giving data.

from lib.singleton import Singleton
from events_microservice.models.event import Event
import datetime as dt


class EventDatorMock(metaclass=Singleton):  
    def __init__(self):
        self.__data = {
            0: Event("Evento 1, un titulo", "Breve (o no tanto) descripcion del evento 1. Relleno de contenido en este evento", dt.date(2020, 1, 1), dt.time(20, 50, 10), "Plaza Mayor 1", "Nadie real1.", "Tema libre1", 0),
            1: Event("Evento 1, un titulo", "Breve (o no tanto) descripcion del evento 1. Relleno de contenido en este evento", dt.date(2020, 1, 1), dt.time(20, 50, 10), "Plaza Mayor 1", "Nadie real1.", "Tema libre1", 1),
            2: Event("Evento 2, dos titulo", "Breve (o no tanto) descripcion del evento dos. Relleno de contenido en este evento", dt.date(2020, 2, 2), dt.time(20, 50, 20), "Plaza Mayor 2", "Nadie real2.", "Tema libre2", 2),
            3: Event("Evento 3, tres titulo", "Breve (o no tanto) descripcion del evento 3. Relleno de contenido en este evento", dt.date(2020, 3, 3), dt.time(20, 50, 30), "Plaza Mayor 3", "Nadie real3.", "Tema libre3", 3),
            4: Event("Evento 4,  cuatro titulo", "Breve (o no tanto) descripcion del evento cuatro. Relleno de contenido en este evento", dt.date(2020, 4, 4), dt.time(20, 50, 40), "Plaza Mayor 4", "Nadie real4.", "Tema libre4", 4),
        }

    def get_all(self): 
        return list(self.__data.values())

    def get_by_id(self, id): 
        if not isinstance(id, int):
            raise AttributeError("Parameter id must be of type integer")
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
            new_id = max(self.__data.keys()) + 1

            new = Event(event.get_title(), event.get_description(), event.get_date(), event.get_time(
            ), event.get_place(), event.get_organizer(), event.get_topics(), new_id)
            self.__data[new_id] = new

            return new

    def delete_by_id(self, id):
        if not isinstance(id, int):
            raise AttributeError("Parameter id must be of type integer")
        if id in self.__data:
            return self.__data.pop(id, None)