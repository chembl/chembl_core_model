chembl_core_model
======

This is chembl_core_model package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package contains Django ORM model for accessing ChEMBL db instance.
Is uses fields defined in django_db_core package.
This model describes all tables in ChEMBL, including COMPOUND_MOLS and COMPOUND_IMAGES and therefore is not suitable for migrations (use chembl_migration_model instead).
Using the model you can create database structure that is extremely similar to the original ChEMBL for all major db backends.