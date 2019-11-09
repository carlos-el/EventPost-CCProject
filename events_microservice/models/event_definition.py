# event_model.py

import datetime as dt

class Event:
    def __init__(self, id, title, description, date, time, place = "", organizer = "", topics = ""):
        if not isinstance(id, int):
            raise AttributeError("Argument 'id' must be an int")

        self.__id = id  
        self.set_title(title)
        self.set_description(description)
        self.set_date(date)
        self.set_time(time)
        self.set_place(place)
        self.__set_organizer(organizer)
        self.__set_topics(topics)


    # private setters
    def __set_organizer(self, organizer = ""):
        if not isinstance(organizer, str):
            raise AttributeError("Argument 'organizer' must be a str")
        if len(organizer) > 50:
            raise ValueError("Argument 'organizer' too long, 50 characters maximum.")

        self.__organizer = organizer

    def __set_topics(self, topics = ""):
        if not isinstance(topics, str):
            raise AttributeError("Argument 'topics' must be a str")
        if len(topics) > 50:
            raise ValueError("Argument 'topics' too long, 50 characters maximum.")
        self.__topics = topics


    # public setters
    def set_title(self, title):
        if not isinstance(title, str):
            raise AttributeError("Argument 'title' must be a str")
        if not title:
            raise ValueError("Argument 'title' can not be an empty str")
        if len(title) > 60:
            raise ValueError("Argument 'title' too long, 60 characters maximum.")

        self.__title = title

    def set_description(self, description):
        if not isinstance(description, str):
            raise AttributeError("Argument 'description' must be a str")
        if not description:
            raise ValueError("Argument 'description' can not be an empty str")
        if len(description) < 60:
            raise ValueError("Argument 'description' too short, 60 characters minimum.")
        if len(description) > 400:
            raise ValueError("Argument 'description' too long, 400 characters maximum.")

        self.__description = description

    def set_date(self, date):
        if not isinstance(date, dt.date):
            raise AttributeError("Argument 'date' must be of type datetime.date")
        if date < dt.date.today():
            raise ValueError("Argument 'date' can not be a past date")

        self.__date = date
    
    def set_time(self, time):
        if not isinstance(time, dt.time):
            raise AttributeError("Argument 'time' must be of type datetime.time")

        self.__time = time

    def set_place(self, place = ""):
        if not isinstance(place, str):
            raise AttributeError("Argument 'place' must be a str")
        if len(place) > 100:
            raise ValueError("Argument 'place' too long, 100 characters maximum.")
        
        self.__place = place


    # getters
    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_place(self):
        return self.__place

    def get_organizer(self):
        return self.__organizer

    def get_topics(self):
        return self.__topics