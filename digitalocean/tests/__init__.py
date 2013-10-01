import json
import os
import unittest

import digitalocean

resources_container = os.path.join(os.path.dirname(__file__), 'resources')
resources_endpoint = lambda path: os.path.join(digitalocean.session.Client.BASE, *path.split('.'))
resources = {}
for r in os.listdir(resources_container):
    with open(os.path.join(resources_container, r)) as fp:
        base = digitalocean.session.Client.BASE
        resources[resources_endpoint(r.rsplit('.', 1)[0])] = fp.read()


def __call__(self, *path, **params):
    url = digitalocean.session.Client.build_url(*path)
    return json.loads(resources[url])

digitalocean.session.Client.__call__ = __call__


class TestCase(unittest.TestCase):
    def setUp(self):
        self.session = digitalocean.Session('', '')
        self.droplet = digitalocean.Droplet(self.session)

