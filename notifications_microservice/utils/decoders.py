import datetime as dt
from notifications_microservice.models.notification import Notification


def serialize(obj):
    if isinstance(obj, dt.date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, dt.time):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


def notification_json_decoder(json):
    id = None

    if 'id' in json.keys():
        id = json['id']

    # Can throw (KeyError, IndexError, TypeError)
    tmp = json["scheduled_time"].split('T')
    tmp2 = tmp[1].split('.')
    date = tmp[0].split('-')
    time = tmp2[0].split(':')
    nt = Notification(json['subject'], json['content'], json['to_mail'], 
                            dt.datetime(int(date[0]), int(date[1]), int(date[2]), 
                            int(time[0]), int(time[1]), int(time[2])), id)

    return nt


