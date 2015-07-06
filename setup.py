#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mnowotka'

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='chembl_core_model',
    version='0.6.1',
    author='Michal Nowotka',
    author_email='mnowotka@ebi.ac.uk',
    description='Core ChEMBL python ORM model',
    url='https://www.ebi.ac.uk/chembl/',
    license='Apache Software License',
    packages=['chembl_core_model',
              'chembl_core_model.models'],
    long_description=open('README.rst').read(),
    install_requires=[
        'chembl_core_db>=0.6.1',
        'pyyaml',
    ],
    package_data={
        'chembl_core_model': ['models/sql/*'],
        },
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Chemistry'],
    zip_safe=False,
)
