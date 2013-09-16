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

    @require('id')
    def destroy(self):
        return self.session.image_destroy(self.id) == 'OK'

    @require('id')
    def transfer(self, region_id):
        return self.Event(**event_id(self.session.image_transfer(self.id, region_id)))


class SSHKey(models.SSHKey):
    def __init__(self, session, **ssh_key):
        self.session = session
        super(SSHKey, self).__init__(**ssh_key)

        self.SSHKey = functools.partial(SSHKey, session)

    @require('id')
    def __call__(self):
        return self.SSHKey(**self.session.ssh_key(self.id))

    def __iter__(self):
        for ssh_key in self.session.ssh_keys():
            yield self.SSHKey(**ssh_key)

    def new(self, name, ssh_pub_key):
        ssh_key = self.session.ssh_key_new(name, ssh_pub_key)
        return self.SSHKey(**ssh_key)

    @require('id')
    def destroy(self):
        return self.session.ssh_key_destroy(self.id) == 'OK'

    @require('id')
    def edit(self, ssh_key_pub):
        return self.SSHKey(**self.session.ssh_key_edit(self.id, ssh_key_pub))


class Record(models.Record):
    def __init__(self, session, **record):
        self.session = session
        super(Record, self).__init__(**record)

        self.Domain = functools.partial(Domain, session)
        self.Record = functools.partial(Record, session)

    @require('domain_id', 'id')
    def __call__(self):
        return self.Record(**self.session.domain_record(self.domain_id, self.id))

    @require('domain_id')
    def __iter__(self):
        for record in self.session.domain_records(self.domain_id):
            yield self.Record(**record)

    def new(self, domain_id, record_type, data, name=None, priority=None, port=None, weight=None):
        record = self.session.domain_record_new(domain_id, record_type, data,
            name=name, priority=priority, port=port, weight=weight)
        return self.Record(**record)

    @require('domain_id', 'id')
    def edit(self, record_type, data, name=None, priority=None, port=None, weight=None):
        record = self.session.domain_record_edit(self.domain_id, self.id, record_type, data,
            name=name, priority=priority, port=port, weight=weight)
        return self.Record(**record)

    @require('domain_id', 'id')
    def destroy(self):
        return self.session.domain_record_destroy(self.domain_id, self.id) == 'OK'


class Domain(models.Domain):
    def __init__(self, session, **domain):
        self.session = session
        super(Domain, self).__init__(**domain)

        self.Domain = functools.partial(Domain, session)
        self.Record = functools.partial(Record, session)

    @require('id')
    def __call__(self):
        return self.Domain(**self.session.domain(self.id))

    def __iter__(self):
        for domain in self.session.domains():
            yield self.Domain(**domain)

    def new(self, name, ip_address):
        domain = self.session.domain_new(name, ip_address)
        return self.Domain(**ssh_key)

    @require('id')
    def destroy(self):
        return self.session.domain_destroy(self.id) == 'OK'

    @require('id')
    def records(self):
        return list(self.Record(domain_id=self.id))


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

    def new(self, name, size_id, image_id, region_id, ssh_key_ids=None, private_networking=None):
        droplet = self.session.droplet_new(name, size_id, image_id, region_id,
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
