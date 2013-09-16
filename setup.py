#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pyocean',
    version='0.1.2',
    description='Digital Ocean API',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/digitalocean',
    packages=['digitalocean']
)
