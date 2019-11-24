import falcon

from notifications_microservice.resources.notification_resource import NotificationResource
from notifications_microservice.resources.notifications_resource import NotificationsResource
from notifications_microservice.models.notification_dator import NotificationDatorMock


api = application = falcon.API()

api.add_route('/notifications', NotificationsResource(NotificationDatorMock()))
api.add_route('/notifications/{id}', NotificationResource(NotificationDatorMock()))