import datetime
from . import utils


class Droplet(object):
    def __init__(self, **droplet):
        self.id = utils.getitem(droplet, 'id', int)
        self.name = droplet.get('name')
        self.status = droplet.get('status')
        self.created_at = utils.getitem(droplet, 'created_at', self.__parse_created_at)

        self.ip_address = droplet.get('ip_address')
        self.private_ip_address = droplet.get('private_ip_address')

        self.image_id = utils.getitem(droplet, 'image_id', int)
        self.size_id = utils.getitem(droplet, 'size_id', int)
        self.region_id = utils.getitem(droplet, 'region_id', int)

        self.backups_active = droplet.get('backups_active')

    @staticmethod
    def __parse_created_at(created_at):
        return datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

    def __repr__(self):
        return '<Droplet: {}>'.format(self.id)


class Event(object):
    def __init__(self, **event):
        self.id = utils.getitem(event, 'id', int)
        self.action_status = event.get('action_status')
        self.droplet_id = utils.getitem(event, 'droplet_id', int)
        self.event_type_id = utils.getitem(event, 'event_type_id', int)
        self.percentage = utils.getitem(event, 'percentage', int)

    def __repr__(self):
        return '<Event: {}>'.format(self.id)


class Size(object):
    def __init__(self, id, **size):
        self.id = utils.getitem(size, 'id', int)
        self.name = size.get('name')
        self.slug = size.get('slug')

        self.memory = size.get('memory')
        self.cp = utils.getitem(size, 'cp', int)
        self.disk = size.get('disk')

        self.cost_per_hour = utils.getitem(size, 'cost_per_hour', float)
        self.cost_per_month = utils.getitem(size, 'cost_per_month', float)

    def __repr__(self):
        return '<Size: {}>'.format(self.id)

