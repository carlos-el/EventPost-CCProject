import falcon

from notifications_microservice.resources.notification_resource import NotificationResource
from notifications_microservice.resources.notifications_resource import NotificationsResource
from notifications_microservice.models.notification_dator import MongoNotificationDator


api = application = falcon.API()

api.add_route('/notifications', NotificationsResource(MongoNotificationDator()))
api.add_route('/notifications/{id}', NotificationResource(MongoNotificationDator()))