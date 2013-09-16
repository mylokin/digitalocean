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
        return '<Droplet: {}>'.format(self.name or self.id)


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
    def __init__(self, **size):
        self.id = utils.getitem(size, 'id', int)
        self.name = size.get('name')
        self.slug = size.get('slug')

        self.memory = size.get('memory')
        self.cp = utils.getitem(size, 'cp', int)
        self.disk = size.get('disk')

        self.cost_per_hour = utils.getitem(size, 'cost_per_hour', float)
        self.cost_per_month = utils.getitem(size, 'cost_per_month', float)

    def __repr__(self):
        return '<Size: {}>'.format(self.name or self.id)


class Region(object):
    def __init__(self, **region):
        self.id = utils.getitem(region, 'id', int)
        self.name = region.get('name')
        self.slug = region.get('slug')

    def __repr__(self):
        return '<Region: {}>'.format(self.name or self.id)


class Image(object):
    def __init__(self, **image):
        self.id = utils.getitem(image, 'id', int)
        self.name = image.get('name')
        self.distribution = image.get('distribution')

    def __repr__(self):
        return '<Image: {}>'.format(self.name or self.id)
