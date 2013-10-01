import functools

from . import models
from . import utils
from .session import Session
from .utils import (
    require,
    event_id,
    docstring,
)

docstring = functools.partial(docstring, Session)

class Event(models.Event, utils.Fetch):
    def __init__(self, session, **event):
        self.session = session
        super(Event, self).__init__(**event)

        self.Event = functools.partial(Event, session)
        self.Droplet = functools.partial(Droplet, session)

    @docstring('event')
    def get(self, event_id):
        return self.Event(**self.session.event(event_id))

    @docstring('event')
    @require('id')
    def fetch(self):
        return self.get(self.id)


class Size(models.Size, utils.Iterator):
    def __init__(self, session, **size):
        self.session = session
        super(Size, self).__init__(**size)

        self.Size = functools.partial(Size, session)

    @docstring('sizes')
    def all(self):
        for size in self.session.sizes():
            yield self.Size(**size)


class Region(models.Region, utils.Iterator):
    def __init__(self, session, **region):
        self.session = session
        super(Region, self).__init__(**region)

        self.Region = functools.partial(Region, session)

    @docstring('regions')
    def all(self):
        for region in self.session.regions():
            yield self.Region(**region)


class Image(models.Image, utils.Iterator, utils.Fetch):
    def __init__(self, session, **image):
        self.session = session
        super(Image, self).__init__(**image)

        self.Image = functools.partial(Image, session)

    @docstring('image')
    def get(self, image_id):
        return self.Image(**self.session.image(image_id))

    @docstring('image')
    @require('id')
    def fetch(self):
        return self.get(self.id)

    @docstring('images')
    def all(self):
        for image in self.session.images():
            yield self.Image(**image)

    def filter(self, filter_):
        for image in self.session.images(filter_=filter_):
            yield self.Image(**image)

    @docstring('image_destroy')
    @require('id')
    def destroy(self):
        return self.session.image_destroy(self.id) == 'OK'

    @docstring('image_transfer')
    @require('id')
    def transfer(self, region_id):
        return self.Event(**event_id(self.session.image_transfer(self.id, region_id)))


class SSHKey(models.SSHKey, utils.Iterator, utils.Fetch):
    def __init__(self, session, **ssh_key):
        self.session = session
        super(SSHKey, self).__init__(**ssh_key)

        self.SSHKey = functools.partial(SSHKey, session)

    @docstring('ssh_key')
    def get(self, ssh_key_id):
        return self.SSHKey(**self.session.ssh_key(ssh_key_id))

    @docstring('ssh_key')
    @require('id')
    def fetch(self):
        return self.get(self.id)

    @docstring('ssh_keys')
    def all(self):
        for ssh_key in self.session.ssh_keys():
            yield self.SSHKey(**ssh_key)

    @docstring('ssh_key_new')
    def new(self, name, ssh_pub_key):
        ssh_key = self.session.ssh_key_new(name, ssh_pub_key)
        return self.SSHKey(**ssh_key)

    @docstring('ssh_key_destroy')
    @require('id')
    def destroy(self):
        return self.session.ssh_key_destroy(self.id) == 'OK'

    @docstring('ssh_key_edit')
    @require('id')
    def edit(self, ssh_key_pub):
        return self.SSHKey(**self.session.ssh_key_edit(self.id, ssh_key_pub))


class Record(models.Record, utils.Iterator, utils.Fetch):
    def __init__(self, session, **record):
        self.session = session
        super(Record, self).__init__(**record)

        self.Domain = functools.partial(Domain, session)
        self.Record = functools.partial(Record, session)

    @docstring('domain_record')
    def get(self, domain_id, record_id):
        return self.Record(**self.session.domain_record(domain_id, record_id))

    @docstring('domain_record')
    @require('domain_id', 'id')
    def fetch(self):
        return self.get(self.domain_id, self.id)


    @docstring('domain_records')
    @require('domain_id')
    def all(self):
        for record in self.session.domain_records(self.domain_id):
            yield self.Record(**record)

    @docstring('domain_record_new')
    def new(self, domain_id, record_type, data, name=None, priority=None, port=None, weight=None):
        record = self.session.domain_record_new(domain_id, record_type, data,
            name=name, priority=priority, port=port, weight=weight)
        return self.Record(**record)

    @docstring('domain_record_edit')
    @require('domain_id', 'id')
    def edit(self, record_type, data, name=None, priority=None, port=None, weight=None):
        record = self.session.domain_record_edit(self.domain_id, self.id, record_type, data,
            name=name, priority=priority, port=port, weight=weight)
        return self.Record(**record)

    @docstring('domain_record_destroy')
    @require('domain_id', 'id')
    def destroy(self):
        return self.session.domain_record_destroy(self.domain_id, self.id) == 'OK'


class Domain(models.Domain, utils.Iterator, utils.Fetch):
    def __init__(self, session, **domain):
        self.session = session
        super(Domain, self).__init__(**domain)

        self.Domain = functools.partial(Domain, session)
        self.Record = functools.partial(Record, session)

    @docstring('domain')
    def get(self, domain_id):
        return self.Domain(**self.session.domain(domain_id))

    @docstring('domain')
    @require('id')
    def fetch(self):
        return self.get(self.id)

    @docstring('domains')
    def all(self):
        for domain in self.session.domains():
            yield self.Domain(**domain)

    @docstring('domain_new')
    def new(self, name, ip_address):
        domain = self.session.domain_new(name, ip_address)
        return self.Domain(**ssh_key)

    @docstring('domain_destroy')
    @require('id')
    def destroy(self):
        return self.session.domain_destroy(self.id) == 'OK'

    @docstring('domain_records')
    @require('id')
    def records(self):
        return list(self.Record(domain_id=self.id))


class Droplet(models.Droplet, utils.Iterator, utils.Fetch):
    def __init__(self, session, **droplet):
        self.session = session
        super(Droplet, self).__init__(**droplet)

        self.Event = functools.partial(Event, session)
        self.Droplet = functools.partial(Droplet, session)

    @docstring('droplet')
    def get(self, droplet_id):
        return self.Droplet(**self.session.droplet(droplet_id))

    @docstring('droplet')
    @require('id')
    def fetch(self):
        return self.get(self.id)

    @docstring('droplets')
    def all(self):
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

    @docstring('droplet_destroy')
    @require('id')
    def destroy(self, scrub_data=None):
        return self.__action('destroy', self.id, scrub_data=scrub_data)

    @docstring('droplet_snapshot')
    @require('id')
    def snapshot(self, name=None):
        return self.__action('snapshot', self.id, name=name)

    @docstring('droplet_resize')
    @require('id')
    def resize(self, size_id):
        return self.__action('resize', self.id, size_id)

    @docstring('droplet_restore')
    @require('id')
    def restore(self, image_id):
        return self.__action('restore', self.id, image_id)

    @docstring('droplet_rebuild')
    @require('id')
    def rebuild(self, image_id):
        return self.__action('rebuild', self.id, image_id)

    @docstring('droplet_rename')
    @require('id')
    def rename(self, name):
        return self.__action('rename', self.id, name)

    @docstring('droplet_power_on')
    @require('id')
    def power_on(self):
        return self.__action('power_on', self.id)

    @docstring('droplet_power_off')
    @require('id')
    def power_off(self):
        return self.__action('power_off', self.id)

    @docstring('droplet_power_cycle')
    @require('id')
    def power_cycle(self):
        return self.__action('power_cycle', self.id)

    @docstring('droplet_reboot')
    @require('id')
    def reboot(self):
        return self.__action('reboot', self.id)

    @docstring('droplet_shutdown')
    @require('id')
    def shutdown(self):
        return self.__action('shutdown', self.id)

    @docstring('droplet_password_reset')
    @require('id')
    def password_reset(self):
        return self.__action('password_reset', self.id)

    @docstring('droplet_enable_backups')
    @require('id')
    def enable_backups(self):
        return self.__action('enable_backups', self.id)

    @docstring('droplet_disable_backups')
    @require('id')
    def disable_backups(self):
        return self.__action('disable_backups', self.id)
