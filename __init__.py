import functools

from . import models
from . import utils
from .session import Session
from .utils import (
    require,
    event_id,
)


class Event(models.Event):
    def __init__(self, session, **event):
        self.session = session
        super(Event, self).__init__(**event)

        self.Event = functools.partial(Event, session)
        self.Droplet = functools.partial(Droplet, session)

    @require('id')
    def __call__(self):
        return self.Event(**self.session.event(self.id))


class Size(models.Size):
    def __init__(self, session, **size):
        self.session = session
        super(Size, self).__init__(**size)

        self.Size = functools.partial(Size, session)

    def __iter__(self):
        for size in self.session.sizes():
            yield self.Size(**size)


class Droplet(models.Droplet):
    ACTIONS = ('power_on', 'power_off', 'power_cycle', 'reboot', 'shutdown', 'password_reset',
        'enable_backups', 'disable_backups')

    def __init__(self, session, **droplet):
        self.session = session
        super(Droplet, self).__init__(**droplet)

        self.Event = functools.partial(Event, session)
        self.Droplet = functools.partial(Droplet, session)

    @require('id')
    def __call__(self):
        return self.Droplet(**self.session.droplet(self.id))

    def __iter__(self):
        for droplet in self.session.droplets():
            yield self.Droplet(**droplet)

    @require('name', 'size_id', 'image_id', 'region_id')
    def new(self, ssh_key_ids=None, private_networking=None):
        droplet = self.session.droplet_new(self.name, self.size_id, self.image_id, self.region_id,
            ssh_key_ids=ssh_key_ids,
            private_networking=private_networking)
        event = self.Event(id=droplet.pop('event_id'))
        droplet = self.Droplet(**droplet)
        return event, droplet

    def __action(self, action, *args, **kwargs):
        action = getattr(self.session, 'droplet_{}'.format(action))
        return self.Event(**event_id(action(*args, **kwargs)))

    @require('id')
    def destroy(self, scrub_data=None):
        return self.__action('destroy', self.id, scrub_data=scrub_data)

    @require('id')
    def snapshot(self, name=None):
        return self.__action('snapshot', self.id, name=name)

    @require('id')
    def resize(self, size_id):
        return self.__action('resize', self.id, size_id)

    @require('id')
    def restore(self, image_id):
        return self.__action('restore', self.id, image_id)

    @require('id')
    def rebuild(self, image_id):
        return self.__action('rebuild', self.id, image_id)

    @require('id')
    def rename(self, name):
        return self.__action('rename', self.id, name)

    def __getattr__(self, name):
        def handler(action):
            return self.Event(**event_id(action(self.id)))

        if name in self.ACTIONS:
            action = getattr(self.session, 'droplet_{}'.format(name))
            if self.id:
                return handler(action)
            else:
                raise AttributeError(self.attribute_error(name))
        else:
            raise AttributeError(self.attribute_error(name))

