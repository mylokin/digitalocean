#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(name='pyocean',
    version='0.1',
    description='Digital Ocean API',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/digitalocean',
    packages=['digitalocean'],
    install_requires=['requests'],
)
