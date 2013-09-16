#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(name='pyocean',
    version='0.1',
    description='Digital Ocean API',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/digitalocean',
    packages=['digitalocean'],
    install_requires=['requests'],
    long_description=long_description
)
