import falcon
import json
from notifications_microservice.models.notification import Notification
from notifications_microservice.utils.decoders import serialize, notification_json_decoder


class NotificationsResource(object):
    def __init__(self, dator):
        self._dator = dator

    def on_get(self, req, resp):
        # Get all notifications
        notifications = self._dator.get_all()

        # Format notifications to json using our serialize funtion
        resp.body = json.dumps(
            [nt.__dict__ for nt in notifications], default=serialize)

    def on_post(self, req, resp):
        # Read request body
        body = req.bounded_stream.read().decode("utf-8")

        # Check body is not empty
        if body is "" or body is None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps(
                {"error": "Data not provided in request body."})
            return resp
        
        # Load notification from json data
        try:
            nt = json.loads(body, object_hook=notification_json_decoder)
        except (KeyError, TypeError, IndexError, AttributeError, ValueError):
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(
                {"error": "Error in data provided in request body."})
            return resp

        # Save notification
        self._dator.save(nt) 
        resp.status = falcon.HTTP_CREATED

        
        

        
        

  


        
