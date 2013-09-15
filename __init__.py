import datetime
import os
import requests

import exceptions


class Client(object):
    BASE = 'https://api.digitalocean.com/'

    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key

    @property
    def params(self):
        return {
            'client_id': self.client_id,
            'api_key': self.api_key
        }

    @classmethod
    def build_url(cls, *path):
        return os.path.join(cls.BASE, *map(str, path))

    def __call__(self, *path, **params):
        url = self.build_url(*path)
        response = requests.get(url, params=dict(self.params, **params))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError, e:
            if e.response.status_code in exceptions.status_codes:
                raise exceptions.status_codes[e.response.status_code](e.message)
            else:
                raise exceptions.Exception(e.message)
        content = response.json()
        print content
        if content['status'] != 'OK':
            raise exceptions.Exception(content['error_message'])
        return content


class API(object):
    def __init__(self, client):
        self.client = client

    def droplet(self, droplet_id):
        ''' Show droplet '''
        return Droplet(**self.client('droplets', droplet_id)['droplet'])

    def droplet_new(self, name, size_id, image_id, region_id, ssh_key_ids=None, private_networking=None):
        ''' New droplet '''
        params = {
            'name': name,
            'size_id': size_id,
            'image_id': image_id,
            'region_id': region_id
        }
        if ssh_key_ids:
            params['ssh_key_ids'] = ssh_key_ids
        if private_networking:
            params['private_networking'] = private_networking

        droplet = self.client('droplets', 'new', **params)['droplet']
        event = Event(droplet.pop('event_id'))
        droplet = Droplet(**droplet)
        return event, droplet

    def droplet_destroy(self, droplet_id, scrub_data=None):
        ''' Destroy Droplet '''
        params = {}
        if scrub_data:
            params['scrub_data'] = scrub_data
        return Event(**{'id': self.client('droplets', droplet_id, 'destroy', **params)['event_id']})

    def droplet_snapshot(self, droplet_id, name=None):
        ''' Take a Snapshot '''
        params = {}
        if name:
            params['name'] = name
        return Event(**{'id': self.client('droplets', droplet_id, 'snapshot', **params)['event_id']})

    def droplet_power_on(self, droplet_id):
        ''' Power On '''
        return Event(**{'id': self.client('droplets', droplet_id, 'power_on', **params)['event_id']})

    def droplet_power_off(self, droplet_id):
        ''' Power off '''
        return Event(**{'id': self.client('droplets', droplet_id, 'power_off', **params)['event_id']})

    def droplet_power_cycle(self, droplet_id):
        ''' Power cycle droplet '''
        return Event(**{'id': self.client('droplets', droplet_id, 'power_cycle', **params)['event_id']})

    def droplet_reboot(self, droplet_id):
        ''' Reboot droplet '''
        return Event(**{'id': self.client('droplets', droplet_id, 'reboot', **params)['event_id']})

    def droplet_shutdown(self, droplet_id):
        ''' Shut down droplet '''
        return Event(**{'id': self.client('droplets', droplet_id, 'shutdown', **params)['event_id']})

    def droplets(self):
        ''' Show all active droplets '''
        return [Droplet(**d) for d in self.client('droplets')['droplets']]

    def event(self, event_id):
        return Event(**self.client('events', event_id)['event'])

    def sizes(self):
        return [Size(**s) for s in self.client('sizes')['sizes']]


class Droplet(object):
    def __init__(self, id, **droplet):
        self.id = int(id)
        self.name = droplet.get('name')
        self.status = droplet.get('status')
        self.created_at = self.__parse_created_at(droplet['created_at']) if 'created_at' in droplet else None

        self.ip_address = droplet.get('ip_address')
        self.private_ip_address = droplet.get('private_ip_address')

        self.image_id = int(droplet['image_id']) if 'image_id' in droplet else None
        self.size_id = int(droplet['size_id']) if 'size_id' in droplet else None
        self.region_id = int(droplet['region_id']) if 'region_id' in droplet else None

        self.backups_active = droplet.get('backups_active')

        self.droplet = droplet

    @staticmethod
    def __parse_created_at(created_at):
        return datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

    def __repr__(self):
        return '<Droplet: {}>'.format(self.id)


class Event(object):
    def __init__(self, id, **event):
        self.id = int(id)
        self.action_status = event.get('action_status')
        self.droplet_id = event.get('droplet_id')
        self.event_type_id = event.get('event_type_id')
        self.percentage = event.get('percentage')

        self.event = event

    def __repr__(self):
        return '<Event: {}>'.format(self.id)


class Size(object):
    def __init__(self, id, **size):
        self.id = int(id)
        self.name = size.get('name')
        self.slug = size.get('slug')

        self.memory = size.get('memory')
        self.cp = int(size['cp']) if 'cp' in size else None
        self.disk = size.get('disk')

        self.cost_per_hour = float(size['cost_per_hour']) if 'cost_per_hour' in size else None
        self.cost_per_month = float(size['cost_per_month']) if 'cost_per_month' in size else None

        self.size = size

    def __repr__(self):
        return '<Size: {}>'.format(self.id)

