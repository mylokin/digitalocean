import digitalocean

from . import TestCase


class DropletTestCase(TestCase):
    DROPLET_ID = 100823

    def test_find(self):
        droplet = self.droplet.find_one(size_id=33)

        self.assertEqual(droplet.size_id, 33)

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

    def test_destroy(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.destroy()

        self.assertEqual(event.id, 7501)

    def test_snapshot(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.snapshot()

        self.assertEqual(event.id, 7501)

    def test_resize(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.resize(55)

        self.assertEqual(event.id, 7501)

    def test_restore(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.restore(420)

        self.assertEqual(event.id, 7501)

    def test_rebuild(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.rebuild(420)

        self.assertEqual(event.id, 7501)

    def test_rename(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.rename('test333')

        self.assertEqual(event.id, 7501)

    def test_power_on(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.power_on()

        self.assertEqual(event.id, 7501)

    def test_power_off(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.power_off()

        self.assertEqual(event.id, 7501)

    def test_power_cycle(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.power_cycle()

        self.assertEqual(event.id, 7501)

    def test_reboot(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.reboot()

        self.assertEqual(event.id, 7501)

    def test_shutdown(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.shutdown()

        self.assertEqual(event.id, 7501)

    def test_password_reset(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.password_reset()

        self.assertEqual(event.id, 7501)

    def test_enable_backups(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.enable_backups()

        self.assertEqual(event.id, 7501)

    def test_disable_backups(self):
        droplet = self.droplet.get(self.DROPLET_ID)
        event = droplet.disable_backups()

        self.assertEqual(event.id, 7501)
