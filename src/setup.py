#!/usr/bin/env python
from distutils.core import setup
setup(name='gandyn',
      version='0.2.1',
      description='Dynamic record update client for the Gandy LiveDNS API.',
      author='Charly Caulet',
      author_email='charly.caulet@no-log.org',
      url='https://github.com/Chralu/gandyn/',
      packages=['ipretriever'],
      scripts=['gandyn.py'],
      )
