import falcon
import json
from events_microservice import settings
from events_microservice.models.event import Event
from events_microservice.utils.decoders import serialize, event_json_decoder

@settings.cache.cached(timeout=1200)
class EventsResource(object):
    def __init__(self, dator):
        self._dator = dator

    def on_get(self, req, resp):
        # Get all events
        events = self._dator.get_all()

        # Format events to json using our serialize funtion
        resp.body = json.dumps(
            [ev.to_json() for ev in events], default=serialize)

    def on_post(self, req, resp):
        # Read request body
        body = req.bounded_stream.read().decode("utf-8")

        # Check body is not empty
        if body is "" or body is None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps(
                {"error": "Data not provided in request body."})
            return resp
        
        # Load event from json data
        try:
            ev = json.loads(body, object_hook=event_json_decoder)
        except (KeyError, TypeError, IndexError, AttributeError, ValueError):
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(
                {"error": "Error in data provided in request body."})
            return resp

        # Save event
        posted_ev = self._dator.save(ev) 
        resp.body = json.dumps(posted_ev.to_json(), default=serialize)
        resp.status = falcon.HTTP_CREATED


        
        

        
        

  


        
