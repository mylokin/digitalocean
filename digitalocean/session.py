import functools

import os
import json
import urllib
import urllib2

from . import exceptions


class Client(object):
    BASE = 'https://api.digitalocean.com/'
    IMAGES_FILTERS = ('my_images', 'global')

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
        params = urllib.urlencode(dict(params, client_id=self.client_id, api_key=self.api_key))
        try:
            response = urllib2.urlopen('{}?{}'.format(url, params)).read()
        except urllib2.HTTPError, e:
            if e.code in exceptions.status_codes:
                raise exceptions.status_codes[e.code](e.message)
            else:
                raise exceptions.Exception(e.message)
        content = json.loads(response)
        if content['status'] != 'OK':
            raise exceptions.Exception(content['error_message'])
        return content


class Session(object):
    def __init__(self, client_id, api_key):
        self.client = Client(client_id, api_key)

    def droplet_action(method):
        @functools.wraps(method)
        def event(self, droplet_id, **params):
            action_name = method(self, **params)
            if isinstance(action_name, tuple):
                action_name, params = action_name
            return self.client('droplets', droplet_id, action_name, **params)
        return event

    def droplet(self, droplet_id):
        ''' Returns full information for a specific droplet ID that is passed in the URL. '''
        return self.client('droplets', droplet_id)['droplet']

    def droplet_new(self, name, size_id, image_id, region_id, ssh_key_ids=None, private_networking=None):
        ''' Create a new droplet. '''
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

        return self.client('droplets', 'new', **params)['droplet']

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
        return 'power_on'

    @droplet_action
    def droplet_power_off(self):
        ''' Poweroff a running droplet. The droplet will remain in your account. '''
        return 'power_off'

    @droplet_action
    def droplet_power_cycle(self):
        ''' Power cycle a droplet. This will turn off the droplet and then turn it back on. '''
        return 'power_cycle'

    @droplet_action
    def droplet_reboot(self):
        ''' Reboot a droplet. This is the preferred method to use if a server is not responding. '''
        return 'reboot'

    @droplet_action
    def droplet_shutdown(self):
        ''' Shutdown a running droplet. The droplet will remain in your account. '''
        return 'shutdown'

    @droplet_action
    def droplet_password_reset(self):
        ''' Reset the root password for a droplet. Please be aware that this will reboot the droplet to allow resetting the password. '''
        return 'password_reset'

    @droplet_action
    def droplet_enable_backups(self):
        ''' Enables automatic backups which run in the background daily to backup your droplet's data. '''
        return 'enable_backups'

    @droplet_action
    def droplet_disable_backups(self):
        ''' Disables automatic backups from running to backup your droplet's data. '''
        return 'disable_backups'

    def droplet_resize(self, droplet_id, size_id):
        ''' Resize a specific droplet to a different size. This will affect the number of processors and memory allocated to the droplet. '''
        return self.client('droplets', droplet_id, 'resize', size_id=size_id)

    def droplet_restore(self, droplet_id, image_id):
        ''' Restore a droplet with a previous image or snapshot. This will be a mirror copy of the image or snapshot to your droplet. Be sure you have backed up any necessary information prior to restore. '''
        return self.client('droplets', droplet_id, 'restore', image_id=image_id)

    def droplet_rebuild(self, droplet_id, image_id):
        ''' Reinstall a droplet with a default image. This is useful if you want to start again but retain the same IP address for your droplet. '''
        return self.client('droplets', droplet_id, 'rebuild', image_id=image_id)

    def droplet_rename(self, droplet_id, name):
        ''' Renames the droplet to the specified name. '''
        return self.client('droplets', droplet_id, 'rename', name=name)

    def droplets(self):
        ''' Returns all active droplets that are currently running in your account. All available API information is presented for each droplet. '''
        return self.client('droplets')['droplets']

    def event(self, event_id):
        ''' Returns all the available sizes that can be used to create a droplet. '''
        return self.client('events', event_id)['event']

    def sizes(self):
        ''' Report on the progress of an event by providing the percentage of completion. '''
        return self.client('sizes')['sizes']

    def regions(self):
        ''' Return all the available regions within the DigitalOcean cloud. '''
        return self.client('regions')['regions']

    def image(self, image_id):
        ''' Displays the attributes of an image. '''
        return self.client('images', image_id)['image']

    def image_destroy(self, image_id):
        ''' Destroy an image. There is no way to restore a deleted image so be careful and ensure your data is properly backed up. '''
        return self.client('images', image_id, 'destroy')['status']

    def image_transfer(self, image_id, region_id):
        ''' Transfer an image to a specified region. '''
        return self.client('images', image_id, 'transfer', region_id=region_id)

    def images(self, filter_=None):
        ''' Returns all the available images that can be accessed by your client ID. You will have access to all public images by default, and any snapshots or backups that you have created in your own account. '''
        params = {}
        if filter_:
            if filter_ not in self.IMAGES_FILTERS:
                raise ValueError('Wrong filter \'{}\''.format(filter_))
            params['filter'] = filter_
        return self.client('images', **params)['images']

    def ssh_key(self, ssh_key_id):
        ''' Shows a specific public SSH key in your account that can be added to a droplet. '''
        return self.client('ssh_keys', ssh_key_id)['ssh_key']

    def ssh_key_new(self, name, ssh_pub_key):
        ''' Add a new public SSH key to your account. '''
        params = {
            'name': name,
            'ssh_pub_key': ssh_pub_key,
        }
        return self.client('ssh_keys', 'new', **params)['ssh_key']

    def ssh_key_destroy(self, ssh_key_id):
        ''' Delete the SSH key from your account. '''
        return self.client('ssh_keys', ssh_key_id, 'destroy')['status']

    def ssh_key_edit(self, ssh_key_id, ssh_key_pub):
        ''' Modify an existing public SSH key in your account. '''
        params = {
            'ssh_key_pub': ssh_key_pub,
        }
        return self.client('ssh_keys', ssh_key_id, 'edit', **params)['ssh_key']

    def ssh_keys(self):
        ''' Lists all the available public SSH keys in your account that can be added to a droplet. '''
        return self.client('ssh_keys')['ssh_keys']

    def domain(self, domain_id):
        ''' Returns the specified domain. '''
        return self.client('domains', domain_id)['domain']

    def domain_new(self, name, ip_address):
        ''' Creates a new domain name with an A record for the specified [ip_address]. '''
        params = {
            'name': name,
            'ip_address': ip_address
        }
        return self.client('domains', 'new', **params)['domain']

    def domain_destroy(self, domain_id):
        ''' Deletes the specified domain. '''
        return self.client('domains', domain_id, 'destroy')['status']

    def domain_record(self, domain_id, record_id):
        ''' Returns the specified domain record. '''
        return self.client('domains', domain_id, 'records', record_id)['record']

    def domain_record_new(self, domain_id, record_type, data, name=None, priority=None, port=None, weight=None):
        ''' Creates a new domain name with an A record for the specified [ip_address]. '''
        params = {
            'record_type': record_type,
            'data': data,
        }
        if name:
            params['name'] = name
        if priority:
            params['priority'] = priority
        if port:
            params['port'] = port
        if weight:
            params['weight'] = weight
        return self.client('domains', domain_id, 'records', 'new', **params)['domain_record']

    def domain_record_edit(self, domain_id, record_id, record_type, data, name=None, priority=None, port=None, weight=None):
        ''' Edits an existing domain record. '''
        params = {
            'record_type': record_type,
            'data': data,
        }
        if name:
            params['name'] = name
        if priority:
            params['priority'] = priority
        if port:
            params['port'] = port
        if weight:
            params['weight'] = weight
        return self.client('domains', domain_id, 'records', record_id, 'edit', **params)['domain_record']

    def domain_record_destroy(self, domain_id, record_id):
        ''' Returns all of your current domain records. '''
        return self.client('domains', domain_id, 'records', record_id, 'destroy')['status']

    def domain_records(self, domain_id):
        ''' Returns all of your current domain records. '''
        return self.client('domains', domain_id, 'records')['records']

    def domains(self):
        ''' Returns all of your current domains. '''
        return self.client('domains')['domains']

