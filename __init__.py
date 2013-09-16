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
        self.session = api
        super(Event, self).__init__(**event)

        self.Event = functools.partial(Event, api)
        self.Droplet = functools.partial(Droplet, api)

    @require(['id'])
    def __call__(self):
        return self.Event(**self.session.event(self.id))


class Size(models.Size):
    def __init__(self, api, **size):
        self.session = api
        super(Size, self).__init__(**size)

        self.Size = functools.partial(Size, api)

    def __iter__(self):
        for size in self.session.sizes():
            yield self.Size(**size)


class Droplet(models.Droplet):
    ACTIONS = ('power_on', 'power_off', 'power_cycle', 'reboot', 'shutdown', 'password_reset',
        'enable_backups', 'disable_backups')

    def __init__(self, api, **droplet):
        self.session = api
        super(Droplet, self).__init__(**droplet)

        self.Event = functools.partial(Event, api)
        self.Droplet = functools.partial(Droplet, api)

    @require(['id'])
    def __call__(self):
        return self.Droplet(**self.session.droplet(self.id))

    def __iter__(self):
        for droplet in self.session.droplets():
            yield self.Droplet(**droplet)

    def __getattr__(self, name):
        def handler(action):
            return self.Event(**event_id(action(self.id)))

        if name in self.ACTIONS:
            action = getattr(self.session, 'droplet_{}'.format(name))
            if self.id:
                return handler(action)
            else:
                raise AttributeError(utils.attribute_error(self, name))
        else:
            raise AttributeError(utils.attribute_error(self, name))


    @require(['name', 'size_id', 'image_id', 'region_id'])
    def new(self, ssh_key_ids=None, private_networking=None):
        droplet = self.session.droplet_new(self.name, self.size_id, self.image_id, self.region_id,
            ssh_key_ids=ssh_key_ids,
            private_networking=private_networking)
        event = self.Event(id=droplet.pop('event_id'))
        droplet = self.Droplet(**droplet)
        return event, droplet

    @require(['id'])
    def destroy(self, scrub_data=None):
        return self.Event(**event_id(self.session.droplet_destroy(self.id, scrub_data=scrub_data)))

    @require(['id'])
    def snapshot(self, name=None):
        return self.Event(**event_id(self.session.droplet_snapshot(self.id, name=name)))

    @require(['id'])
    def resize(self, size_id):
        return self.Event(**event_id(self.session.droplet_resize(self.id, size_id)))

    @require(['id'])
    def restore(self, image_id):
        return self.Event(**event_id(self.session.droplet_restore(self.id, image_id)))

    @require(['id'])
    def rebuild(self, image_id):
        return self.Event(**event_id(self.session.droplet_rebuild(self.id, image_id)))

    @require(['id'])
    def rename(self, name):
        return self.Event(**event_id(self.session.droplet_rename(self.id, name)))
