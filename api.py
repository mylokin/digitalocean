import functools


class API(object):
    def __init__(self, client):
        self.client = client

    def droplet_action(method):
        @functools.wraps(method)
        def event(self, droplet_id, **params):
            action_name = method(self, **params)
            if isinstance(action_name, list):
                action_name, params = action_name
            return self.client('droplets', droplet_id, action_name, **params)
        return event

    def droplet(self, droplet_id):
        ''' Returns full information for a specific droplet ID that is passed in the URL. '''
        return self.client('droplets', droplet_id)['droplet']
        # return Droplet(**self.client('droplets', droplet_id)['droplet'])

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

        # droplet = self.client('droplets', 'new', **params)['droplet']
        # event = Event(droplet.pop('event_id'))
        # droplet = Droplet(**droplet)
        # return event, droplet

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

    def droplets(self):
        ''' Returns all active droplets that are currently running in your account. All available API information is presented for each droplet. '''
        return self.client('droplets')['droplets']
        # return [Droplet(**d) for d in self.client('droplets')['droplets']]

    def event(self, event_id):
        return self.client('events', event_id)['event']
        # return Event(**self.client('events', event_id)['event'])

    def sizes(self):
        return self.client('sizes')['sizes']
        # return [Size(**s) for s in self.client('sizes')['sizes']]
