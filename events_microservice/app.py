import falcon

from events_microservice.resources.events_resource import EventsResource
from events_microservice.resources.event_resource import EventResource
from events_microservice.models.event_dator import EventDatorMock 


api = application = falcon.API()

api.add_route('/events', EventsResource(EventDatorMock()))
api.add_route('/events/{id}', EventResource(EventDatorMock()))