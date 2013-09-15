import functools

from . import models
from .api import API
from .utils import require, event_id


class Event(models.Event):
    def __init__(self, api, **event):
        self.__api = api
        super(Event, self).__init__(**event)

        self.Event = functools.partial(Event, api)
        self.Droplet = functools.partial(Droplet, api)

    @require(['id'])
    def __call__(self):
        return self.Event(**self.__api.event(self.id))


class Droplet(models.Droplet):
    def __init__(self, api, **droplet):
        self.__api = api
        super(Droplet, self).__init__(**droplet)

        self.Event = functools.partial(Event, api)
        self.Droplet = functools.partial(Droplet, api)

    @require(['id'])
    def __call__(self):
        return self.Droplet(**self.__api.droplet(self.id))

    def __iter__(self):
        for droplet in self.__api.droplets():
            yield self.Droplet(**droplet)

    @require(['name', 'size_id', 'image_id', 'region_id'])
    def new(self, ssh_key_ids=None, private_networking=None):
        droplet = self.__api.droplet_new(self.name, self.size_id, self.image_id, self.region_id,
            ssh_key_ids=ssh_key_ids,
            private_networking=private_networking)
        event = self.Event(id=droplet.pop('event_id'))
        droplet = self.Droplet(**droplet)
        return event, droplet


    @require(['id'])
    def destroy(self, scrub_data=None):
        return self.Event(**event_id(self.__api.droplet_destroy(self.id, scrub_data=scrub_data)))

    @require(['id'])
    def power_on(self):
        return self.Event(**event_id(self.__api.droplet_power_on(self.id)))

    @require(['id'])
    def power_off(self):
        return self.Event(**event_id(self.__api.droplet_power_off(self.id)))


