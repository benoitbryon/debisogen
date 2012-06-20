# coding=utf-8
import os

from setuptools import setup, find_packages


def read_relative_file(filename):
    """Returns contents of the given file.
    Filename argument must be relative to this module.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(name='marmelune.debianisobuilder',
      version=read_relative_file('version.txt'),
      description='Experimental scripts, files and templates around ' \
                  'Debian installer.',
      long_description=read_relative_file('README.rst'),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning'
        ],
      keywords="",
      author='Benoît Bryon',
      author_email='benoit@marmelune.net',
      url='https://github.com/benoitbryon',
      license='BSD',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'': 'src'},
      namespace_packages=['marmelune'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'PasteScript', 'Cheetah'],
      entry_points=""" # -*- Entry points: -*-
      [paste.paster_create_template]
      marmelune_debian_preseed = marmelune.debianisobuilder.pastescript:DebianPreseedTemplate
      [console_scripts]
      debianisobuilder = marmelune.debianisobuilder.commands:build_iso
      """,
      )
