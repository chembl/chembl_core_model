#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mnowotka'

import sys

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

if sys.version_info < (2, 7, 3) or sys.version_info >= (3, 0, 0):
    raise Exception('ChEMBL software stack requires python 2.7.3 - 2.7.7')

setup(
    name='chembl_core_model',
    version='0.5.11',
    author='Michal Nowotka',
    author_email='mnowotka@ebi.ac.uk',
    description='Core ChEMBL python ORM model',
    url='https://www.ebi.ac.uk/chembl/',
    license='CC BY-SA 3.0',
    packages=['chembl_core_model',
              'chembl_core_model.models'],
    long_description=open('README.rst').read(),
    install_requires=[
        'chembl_core_db>=0.5.8'
    ],
    package_data={
        'chembl_core_model': ['models/sql/*'],
        },
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: Creative Commons :: Attribution-ShareAlike 3.0 Unported',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Chemistry'],
    zip_safe=False,
)
