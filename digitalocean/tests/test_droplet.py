import digitalocean

from . import TestCase


class DropletTestCase(TestCase):
    def test_list(self):
        droplets = list(self.droplet)

        self.assertEqual(len(droplets), 1)
        self.assertTrue(hasattr(droplets[0], 'session'))

    def test_new(self):
        event, droplet = self.droplet.new('test', 32, 419, 55)

        self.assertEqual(event.id, 7499)
        self.assertEqual(droplet.name, 'test')

    def test_droplet(self):
        droplet = self.droplet
        droplet.id = 100823
        droplet = droplet()

        self.assertEqual(droplet.name, 'test222')
