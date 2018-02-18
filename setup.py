#!/usr/bin/env python

from setuptools import find_packages, setup

about = {}
with open('gpmplgen/__version__.py') as f:
    exec(f.read(), about)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='GPM-Playlist-Generator',
      version=about['__version__'],
      description='Google Play Music - Playlist Generator',
      long_description = readme(),
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
      keywords=['google music', 'google play music', 'playlist', 'playlist generator'],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Multimedia :: Sound/Audio',
      ]
      )
