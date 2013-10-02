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

    image = [i for i in list(digitalocean.Image(session)) if i.name == image][0]
    region = [r for r in list(digitalocean.Region(session)) if r.slug == region][0]
    size = [s for s in list(digitalocean.Size(session)) if s.name == size][0]
    ssh_key = [s for s in list(digitalocean.SSHKey(session)) if s.name == ssh_key][0]

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

