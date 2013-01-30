#!/usr/bin/python2.4

""" The setup and build script for the python-analysis-croatia repository.
    Copyright (C) 2012./2013. Aleksandar Gavrilovic / FER

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__ = 'Aleksandar Gavrilovic'
__version__ = '0.1dev'

# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
  name = "twitter-analysis-croatia",
  version = __version__,
  py_modules = ['twitterCommunication','twitterDB'],
  author='Aleksandar Gavrilović',
  author_email='aleksandar.gavrilovic@fer.hr',
  description='College project for analysing data from Twitter',
  license='GPL',
  url='https://github.com/agavrilovic/twitter-analysis-croatia',
  keywords='twitter analysis croatia',
)

# Extra package metadata to be used only if setuptools is installed
SETUPTOOLS_METADATA = dict(
  install_requires = ['setuptools'],
  include_package_data = True,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GPL Software License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: Twitter',
  ],
  #test_suite = 'twitter-analysis-croatia_test.suite',
)

def Read(file):
  return open(file).read()

def Main():
  # Build the long_description from the README and CHANGES
  METADATA['long_description'] = Read('README.md')

  # Use setuptools if available, otherwise fallback and use distutils
  try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
  except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)


if __name__ == '__main__':
  Main()