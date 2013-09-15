import functools
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

    def droplet_action(method):
        @functools.wraps(method)
        def event(self, droplet_id, **params):
            action_name, params = method(self, **params)
            return Event(**{'id': self.client('droplets', droplet_id, action_name, **params)['event_id']})
        return event

    def droplet(self, droplet_id):
        ''' Returns full information for a specific droplet ID that is passed in the URL. '''
        return Droplet(**self.client('droplets', droplet_id)['droplet'])

    def droplet_new(self, name, size_id, image_id, region_id, ssh_key_ids=None, private_networking=None):
        '''  Create a new droplet. '''
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

    @droplet_action
    def droplet_destroy(self, scrub_data=None):
        '''  Destroys one of your droplets - this is irreversible. '''
        params = {}
        if scrub_data:
            params['scrub_data'] = scrub_data
        return 'destroy', params

    @droplet_action
    def droplet_snapshot(self, name=None):
        '''  Take a snapshot of the droplet once it has been powered off, which can later be restored or used to create a new droplet from the same image. Please be aware this may cause a reboot. '''
        params = {}
        if name:
            params['name'] = name
        return 'snapshot', params

    @droplet_action
    def droplet_power_on(self):
        ''' Poweron a powered off droplet. '''
        return 'power_on', {}

    @droplet_action
    def droplet_power_off(self):
        ''' Poweroff a running droplet. The droplet will remain in your account. '''
        return 'power_off', {}

    @droplet_action
    def droplet_power_cycle(self):
        ''' Power cycle a droplet. This will turn off the droplet and then turn it back on. '''
        return 'power_cycle', {}

    @droplet_action
    def droplet_reboot(self):
        ''' Reboot a droplet. This is the preferred method to use if a server is not responding. '''
        return 'reboot', {}

    @droplet_action
    def droplet_shutdown(self):
        ''' Shutdown a running droplet. The droplet will remain in your account. '''
        return 'shutdown', {}

    @droplet_action
    def droplet_password_reset(self):
        ''' Reset the root password for a droplet. Please be aware that this will reboot the droplet to allow resetting the password. '''
        return 'password_reset', {}

    def droplets(self):
        ''' Returns all active droplets that are currently running in your account. All available API information is presented for each droplet. '''
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

