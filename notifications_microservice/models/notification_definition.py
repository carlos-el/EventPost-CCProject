## notification_model.py

import datetime as dt
import re

class Notification:
    def __init__(self, id, subject, content, to_mail, scheduled_time):
        if not isinstance(id, int):
            raise AttributeError("Argument 'id' must be an int")

        self.set_subject(subject)
        self.set_content(content)
        self.set_to_mail(to_mail)
        self.set_scheduled_time(scheduled_time)

    # setters
    def set_subject(self, subject):
        if not isinstance(subject, str):
            raise AttributeError("Argument 'subject' in Notification must be a str")
        if len(subject) < 10:
            raise ValueError("Argument 'subject' in Notification too short, 10 characters minimum.") 
        if len(subject) > 70:
            raise ValueError("Argument 'subject' in Notification too long, 70 characters maximum.")   
        
        self.__subject = subject

    def set_content(self, content):
        if not isinstance(content, str):
            raise AttributeError("Argument 'content' in Notification must be a str")
        if len(content) < 30:
            raise ValueError("Argument 'content' in Notification too short, 30 characters minimum.") 
        if len(content) > 700:
            raise ValueError("Argument 'content' in Notification too long, 700 characters maximum.")   

        self.__content = content

    def set_to_mail(self, to_mail):
        if not isinstance(to_mail, str):
            raise AttributeError("Argument 'to_mail' in Notification must be a str")
        if None == re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", to_mail):
            raise ValueError("Argument 'to_mail' in Notification must be a valid email.") 

        self.__to_mail = to_mail

    def set_scheduled_time(self, scheduled_time):
        if not isinstance(scheduled_time, dt.datetime):
            raise AttributeError("Argument 'scheduled_time' in Notification must be of type datetime.datetime")
        if not scheduled_time > dt.datetime.now():
            raise ValueError("Argument 'scheduled time' in Notification must be grater than current time.") 
    
        self.__scheduled_time = scheduled_time

    
    # getters
    def get_id(self):
        return self.__id
    
    def get_subject(self):
        return self.__subject
    
    def get_content(self):
        return self.__content

    def get_to_mail(self):
        return self.__to_mail

    def get_scheduled_time(self):
        return self.__scheduled_time