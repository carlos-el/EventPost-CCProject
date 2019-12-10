import falcon
import json
from notifications_microservice.models.notification import Notification
from notifications_microservice.utils.decoders import serialize, notification_json_decoder


class NotificationResource(object):
    def __init__(self, dator):
        self._dator = dator

    def on_get(self, req, resp, id):
        # Check id exist
        try:
            nt = self._dator.get_by_id(int(id))
        except ValueError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps(
                {"error": "Resource with specified Id does not exist."})
            return resp

        resp.body = json.dumps(nt.__dict__, default=serialize)

    def on_put(self, req, resp, id):
        # Check that the notification specified exist
        try:
            nt = self._dator.get_by_id(int(id))
        except ValueError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps(
                {"error": "Resource with specified Id does not exist."})
            return resp

        # Read body of the request with the new notification data
        body = req.bounded_stream.read().decode("utf-8")

        # Check body is not empty
        if body is "" or body is None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps(
                {"error": "Data not provided in request body."})
            return resp

        # Load notification from body data if it is well formatted.
        try:
            nt = json.loads(body, object_hook=notification_json_decoder)
        except:
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(
                {"error": "Error in data provided in request body."})
            return resp

        # Create the edited notification checking that the id is right
        new_nt = Notification(nt.get_subject(), nt.get_content(), nt.get_to_mail(), nt.get_scheduled_time(), int(id))
        # Save edited event
        self._dator.save(new_nt)
