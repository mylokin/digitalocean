import digitalocean

from . import TestCase


class DropletTestCase(TestCase):
    def test_all(self):
        droplets = list(self.droplet)

        self.assertEqual(len(droplets), 1)
        self.assertTrue(hasattr(droplets[0], 'session'))

    def test_new(self):
        event, droplet = self.droplet.new('test', 32, 419, 55)

        self.assertEqual(event.id, 7499)
        self.assertEqual(droplet.name, 'test')

    def test_fetch(self):
        droplet = self.droplet
        droplet.id = 100823
        droplet = droplet()

        self.assertEqual(droplet.name, 'test222')

    def test_get(self):
        droplet = self.droplet.get(100823)

        self.assertEqual(droplet.name, 'test222')
