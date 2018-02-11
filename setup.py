#!/usr/bin/env python

from setuptools import find_packages, setup

about = {}
with open('gpmplgen/__version__.py') as f:
    exec(f.read(), about)

setup(name='GPM-Playlist-Generator',
      version=about['__version__'],
      description='Google Play Music - Playlist Generator',
      author='Hugo Haas',
      author_email='hugoh@hugoh.net',
      url='https://gitlab.com/hugoh/gpm-playlistgen',
      packages=find_packages(exclude=('tests',)),
      scripts=[
          'scripts/gpm-playlistgen.py'
      ],
      install_requires=[
          'gmusicapi',
          'pyyaml'
      ],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ]
      )