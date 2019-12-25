import falcon
import json
from events_microservice.models.event import Event
from events_microservice.utils.decoders import serialize, event_json_decoder


class EventResource(object):
    def __init__(self, dator):
        self._dator = dator

    def on_get(self, req, resp, id):
        # Check id exist
        try:
            ev = self._dator.get_by_id(id)
        except ValueError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps(
                {"error": "Resource with specified Id does not exist."})
            return resp

        resp.body = json.dumps(ev.__dict__, default=serialize)

    def on_put(self, req, resp, id):
        # Check that the event specified exist
        try:
            ev = self._dator.get_by_id(id)
        except ValueError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps(
                {"error": "Resource with specified Id does not exist."})
            return resp

        # Read body of the request with the new event data
        body = req.bounded_stream.read().decode("utf-8")

        # Check body is not empty
        if body is "" or body is None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps(
                {"error": "Data not provided in request body."})
            return resp

        # Load event from body data if it is well formatted.
        try:
            ev = json.loads(body, object_hook=event_json_decoder)
        except:
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(
                {"error": "Error in data provided in request body."})
            return resp

        # Create the edited event checking that the id is right
        new_ev = Event(ev.get_title(), ev.get_description(), ev.get_date(
        ), ev.get_time(), ev.get_place(), ev.get_organizer(), ev.get_topics(), id)
        # Save edited event
        self._dator.save(new_ev)
