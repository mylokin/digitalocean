import digitalocean

from . import TestCase


class DropletTestCase(TestCase):
    DROPLET_ID = 100823

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
        droplet.id = self.DROPLET_ID
        droplet = droplet()

        self.assertEqual(droplet.name, 'test222')

    def test_get(self):
        droplet = self.droplet.get(self.DROPLET_ID)

        self.assertEqual(droplet.name, 'test222')

    def test_reboot(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.reboot()

        self.assertEqual(event.id, 7501)
