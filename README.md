# Digital Ocean API [![Build Status](https://travis-ci.org/mylokin/digitalocean.png?branch=master)](https://travis-ci.org/mylokin/digitalocean)

Example 1. How-to create CentOS droplet:

```python
import os
import time

import digitalocean


def create_centos_server(name, image='CentOS 6.4 x32', region='nyc2', size='512MB', ssh_key='mylokin@me.com'):
    ''' Create CentOS 6.4 server '''
    session = digitalocean.Session(
        os.environ['DIGITAL_OCEAN_CLIENT_ID'],
        os.environ['DIGITAL_OCEAN_API_KEY']
    )

    image = digitalocean.Image(session).find_one(name=image)
    region = digitalocean.Region(session).find_one(slug=region)
    size = digitalocean.Size(session).find_one(name=size)
    ssh_key = digitalocean.SSHKey(session).find_one(name=ssh_key)

    print 'Creating droplet: {}'.format(image.name)
    droplets = digitalocean.Droplet(session)
    event, droplet = droplets.new(name, size.id, image.id, region.id, ssh_key_ids=str(ssh_key.id))

    while event().action_status != 'done':
        time.sleep(1)

    print 'Waiting for server: {}'.format(droplet.name)
    time.sleep(15)  # Wait before proceed
    droplet = droplet()  # Update information

    print 'Done: ssh root@{}'.format(droplet.ip_address)
```

