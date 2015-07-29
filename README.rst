chembl_core_model
======

.. image:: https://img.shields.io/pypi/v/chembl_core_model.svg
    :target: https://pypi.python.org/pypi/chembl_core_model/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/chembl_core_model.svg
    :target: https://pypi.python.org/pypi/chembl_core_model/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/chembl_core_model.svg
    :target: https://pypi.python.org/pypi/chembl_core_model/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/chembl_core_model.svg
    :target: https://pypi.python.org/pypi/chembl_core_model/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/chembl_core_model.svg
    :target: https://pypi.python.org/pypi/chembl_core_model/
    :alt: License
    
.. image:: https://badge.waffle.io/chembl/chembl_core_model.png?label=ready&title=Ready 
 :target: https://waffle.io/chembl/chembl_core_model
 :alt: 'Stories in Ready'    

This is chembl_core_model package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package contains Django ORM model for accessing ChEMBL db instance.
Is uses fields defined in django_db_core package.
This model describes all tables in ChEMBL, including COMPOUND_MOLS and COMPOUND_IMAGES and therefore is not suitable for migrations (use chembl_migration_model instead).
Using the model you can create database structure that is extremely similar to the original ChEMBL for all major db backends.
