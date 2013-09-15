import functools

from . import models
from . import utils
from .api import API
from .utils import (
    require,
    event_id,
    attribute_error,
)


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
    ACTIONS = ('power_on', 'power_off', 'power_cycle', 'reboot', 'shutdown', 'password_reset',
        'enable_backups', 'disable_backups')

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

    def __getattr__(self, name):
        def handler(action):
            return self.Event(**event_id(action(self.id)))

        if name in self.ACTIONS:
            action = getattr(self.__api, 'droplet_{}'.format(name))
            if self.id:
                return handler(action)
            else:
                raise AttributeError(utils.attribute_error(self, name))
        else:
            raise AttributeError(utils.attribute_error(self, name))


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


