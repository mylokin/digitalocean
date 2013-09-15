class Droplet(object):
    def __init__(self, **droplet):
        self.id = int(droplet.get('id'))
        self.name = droplet.get('name')
        self.status = droplet.get('status')
        self.created_at = self.__parse_created_at(droplet['created_at']) if 'created_at' in droplet else None

        self.ip_address = droplet.get('ip_address')
        self.private_ip_address = droplet.get('private_ip_address')

        self.image_id = int(droplet['image_id']) if 'image_id' in droplet else None
        self.size_id = int(droplet['size_id']) if 'size_id' in droplet else None
        self.region_id = int(droplet['region_id']) if 'region_id' in droplet else None

        self.backups_active = droplet.get('backups_active')

        self.extra = droplet

    @staticmethod
    def __parse_created_at(created_at):
        return datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

    def __repr__(self):
        return '<Droplet: {}>'.format(self.id)


class Event(object):
    def __init__(self, **event):
        self.id = int(event.get('id'))
        self.action_status = event.get('action_status')
        self.droplet_id = int(event.get('droplet_id'))
        self.event_type_id = int(event.get('event_type_id'))
        self.percentage = event.get('percentage')

        self.extra = event

    def __repr__(self):
        return '<Event: {}>'.format(self.id)


class Size(object):
    def __init__(self, id, **size):
        self.id = int(size.get('id'))
        self.name = size.get('name')
        self.slug = size.get('slug')

        self.memory = size.get('memory')
        self.cp = int(size['cp']) if 'cp' in size else None
        self.disk = size.get('disk')

        self.cost_per_hour = float(size['cost_per_hour']) if 'cost_per_hour' in size else None
        self.cost_per_month = float(size['cost_per_month']) if 'cost_per_month' in size else None

        self.extra = size

    def __repr__(self):
        return '<Size: {}>'.format(self.id)

