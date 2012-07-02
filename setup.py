#!/usr/bin/env python
# coding=utf-8
import os

from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file.
    Filename argument must be relative to this module.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


README = read_relative_file('README.rst')
VERSION = read_relative_file('version.txt').strip()
NAME = 'debisogen'


setup(name=NAME,
      version=VERSION,
      description='Embed preseed files in ISO images of Debian installer.',
      long_description=README,
      classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
      ],
      keywords="Debian iso preseed",
      author='Benoît Bryon',
      author_email='benoit@marmelune.net',
      url='https://github.com/benoitbryon/debisogen',
      license='BSD',
      packages=[NAME],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'PasteScript', 'Cheetah'],
      entry_points={
          'paste.paster_create_template': [
              'debian_preseed = debisogen.pastescript:DebianPreseedTemplate',
              ],
          'console_scripts': [
              'debisogen = debisogen.commands:build_iso',
          ],
      },
      )
