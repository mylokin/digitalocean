import functools
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
