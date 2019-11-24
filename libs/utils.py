import datetime as dt
from events_microservice.models.event import Event
from notifications_microservice.models.notification import Notification


def serialize(obj):
    if isinstance(obj, dt.date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, dt.time):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


def event_json_decoder(json):
    id = None
    topics = ""
    organizer = ""
    place = ""

    if 'id' in json.keys():
        id = json['id']
    if 'topics' in json.keys():
        topics = json['topics']
    if 'organizer' in json.keys():
        organizer = json['organizer']
    if 'place' in json.keys():
        place = json['place']

    # Can throw (KeyError, IndexError, TypeError)
    date = json['date'].split('-')
    time = json['time'].split(':')
    ev = Event(json['title'], json['description'], dt.date(int(date[0]), int(date[1]), int(date[2])), dt.time(
        int(time[0]), int(time[1]), int(time[2])), place, organizer, topics, id)

    return ev


def notification_json_decoder(json):
    id = None

    if 'id' in json.keys():
        id = json['id']

    # Can throw (KeyError, IndexError, TypeError)
    date = json['date'].split('-')
    time = json['time'].split(':')
    nt = Notification(json['subject'], json['content'], json['to_mail'], dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])), id)

    return nt


