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


class Region(models.Region):
    def __init__(self, session, **region):
        self.session = session
        super(Region, self).__init__(**region)

        self.Region = functools.partial(Region, session)

    def __iter__(self):
        for region in self.session.regions():
            yield self.Region(**region)


class Image(models.Image):
    def __init__(self, session, **image):
        self.session = session
        super(Image, self).__init__(**image)

        self.Image = functools.partial(Image, session)

    @require('id')
    def __call__(self):
        return self.Image(**self.session.image(self.id))

    def __iter__(self):
        for image in self.session.images():
            yield self.Image(**image)

    def filter(self, filter_):
        for image in self.session.images(filter_=filter_):
            yield self.Image(**image)


class Droplet(models.Droplet):
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

    @require('id')
    def power_on(self):
        return self.__action('power_on', self.id)

    @require('id')
    def power_off(self):
        return self.__action('power_off', self.id)

    @require('id')
    def power_cycle(self):
        return self.__action('power_cycle', self.id)

    @require('id')
    def reboot(self):
        return self.__action('reboot', self.id)

    @require('id')
    def shutdown(self):
        return self.__action('shutdown', self.id)

    @require('id')
    def password_reset(self):
        return self.__action('password_reset', self.id)

    @require('id')
    def enable_backups(self):
        return self.__action('enable_backups', self.id)

    @require('id')
    def disable_backups(self):
        return self.__action('disable_backups', self.id)
