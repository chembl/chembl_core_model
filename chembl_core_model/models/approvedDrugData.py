__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

#-----------------------------------------------------------------------------------------------------------------------

class Products(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    AD_TYPE_CHOICES = (
        ('OTC', 'OTC'),
        ('RX', 'RX'),
        ('DISCN', 'DISCN'),
        )

    INFORMATION_SOURCE_CHOICES = (
        ('CBER', 'CBER'),
        ('CDER', 'CDER'),
        ('MANUAL', 'MANUAL'),
        ('ORANGE BOOK', 'ORANGE BOOK'),
        )

    PRODUCT_CLASS_CHOICES = (
        ('VACCINE', 'Vaccine'),
        ('ANTI-RHESIS ANTIBODY', 'Anti-rhesis antibody'),
        )

    NDA_TYPE_CHOICES = (
        ('A', 'A'),
        ('N', 'N'),
        )

    dosage_form = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'The dosage form of the product (e.g., tablet, capsule etc)')
    route = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'The administration route of the product (e.g., oral, injection etc)')
    trade_name = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'The trade name for the product')
    approval_date = ChemblDateField(blank=True, null=True, help_text=u'The FDA approval date for the product (not necessarily first approval of the active ingredient)')
    ad_type = ChemblCharField(max_length=5, blank=True, null=True, choices=AD_TYPE_CHOICES, help_text=u'RX = prescription, OTC = over the counter, DISCN = discontinued')
    oral = ChemblNullableBooleanField(help_text=u'Flag to show whether product is orally delivered')
    topical = ChemblNullableBooleanField(help_text=u'Flag to show whether product is topically delivered')
    parenteral = ChemblNullableBooleanField(help_text=u'Flag to show whether product is parenterally delivered')
    information_source = ChemblCharField(max_length=100, blank=True, null=True, choices=INFORMATION_SOURCE_CHOICES, help_text=u'Source of the product information (e.g., Orange Book)')
    black_box_warning = ChemblNullableBooleanField(help_text=u'Flag to show whether the product label has a black box warning')
    product_class = ChemblCharField(max_length=30, blank=True, null=True, choices=PRODUCT_CLASS_CHOICES)
    applicant_full_name = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Name of the company applying for FDA approval')
    innovator_company = ChemblNullableBooleanField(help_text=u'Flag to show whether the applicant is the innovator of the product')
    product_id = ChemblCharField(primary_key=True, max_length=30, help_text=u'FDA application number for the product')
    load_date = ChemblDateField(blank=True, null=True, help_text=u'The date on which one or more of the following fields were created or updated: doasge_form, route, trade_name, approval_date, ad_type, oral, topical, parenteral, information_source, or applicant_full_name). This date is assigned by the EBI parser.')
    removed_date = ChemblDateField(blank=True, null=True, help_text=u"The date on which this product was first identified (by ebi parser) as having been removed from the information source. The recording of this date was first initiated on 30-JUN-10. Note that a small number of products are removed from OB, but then re-appear... in these cases this field is re-set to 'null' when the product re-appears..")
    nda_type = ChemblCharField(max_length=10, blank=True, null=True, choices=NDA_TYPE_CHOICES, help_text=u'New Drug Application Type. The type of new drug application approval.  New Drug Applications (NDA or innovator)  are "N".   Abbreviated New Drug Applications (ANDA or generic) are "A".') # TODO: 10 for storing one character sounds strange...
    tmp_ingred_count = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text=u'Number of ingredients in the product, to show which are combinations')
    exclude = ChemblIntegerField(length=1, blank=True, null=True, help_text=u'Non-FDA products, to be excluded')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class AtcClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    who_name = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'WHO/INN name for the compound')
    level1 = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'First level of classification')
    level2 = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'Second level of classification')
    level3 = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'Third level of classification')
    level4 = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'Fourth level of classification')
    level5 = ChemblCharField(primary_key=True, max_length=10, help_text=u'Complete ATC code for compound')
    who_id = ChemblCharField(max_length=15, blank=True, null=True, help_text=u'WHO Identifier for compound')
    level1_description = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Description of first level of classification')
    level2_description = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Description of second level of classification')
    level3_description = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Description of third level of classification')
    level4_description = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Description of fourth level of classification')
    molecules = models.ManyToManyField(MoleculeDictionary, through='MoleculeAtcClassification')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class UsanStems(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):


    MAJOR_CLASS_CHOICES = (
        ('GPCR', 'GPCR'),
        ('NR', 'NR'),
        ('PDE', 'PDE'),
        ('ion channel', 'ion channel'),
        ('kinase', 'kinase'),
        ('protease', 'protease'),
        )

    STEM_CLASS_CHOICES = (
        ('Suffix', 'Suffix'),
        ('Prefix', 'Prefix'),
        ('Infix', 'Infix'),
    )

    usan_stem_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Numeric primary key.')
    stem = ChemblCharField(max_length=100, help_text=u'Stem defined for use in United States Adopted Names.')
    subgroup = ChemblCharField(max_length=100, help_text=u'More specific subgroup of the stem defined for use in United States Adopted Names.')
    annotation = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'Meaning of the stem (e.g., the class of compound it applies to).')
    stem_class = ChemblCharField(max_length=100, blank=True, null=True, choices=STEM_CLASS_CHOICES, help_text=u'Indicates whether stem is used as a Prefix/Infix/Suffix.') # TODO: 100 is too long for the specified choices
    major_class = ChemblCharField(max_length=100, blank=True, null=True, choices=MAJOR_CLASS_CHOICES, help_text=u'Protein family targeted by compounds of this class (e.g., GPCR/Ion channel/Protease) where known/applicable.')
    who_extra = ChemblNullableBooleanField(default=False, help_text=u'Stem not represented in USAN list, but added from WHO INN stem list (where set to 1).')
    downgraded = ChemblNullableBooleanField(default=False, help_text=u'Stem no longer included in USAN listing (where set to 1).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("stem", "subgroup"),  )

#-----------------------------------------------------------------------------------------------------------------------

class DefinedDailyDose(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    DDD_UNITS_CHOICES = (
        ('LSU', 'LSU'),
        ('MU', 'MU'),
        ('TU', 'TU'),
        ('U', 'U'),
        ('g', 'g'),
        ('mcg', 'mcg'),
        ('mg', 'mg'),
        ('ml', 'ml'),
        ('mmol', 'mmol'),
        ('tablet', 'tablet'),
        )

    atc_code = models.ForeignKey(AtcClassification, db_column='atc_code', help_text=u'ATC code for the compound (foreign key to ATC_CLASSIFICATION table)')
    ddd_value = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Value of defined daily dose')
    ddd_units = ChemblCharField(max_length=20, blank=True, null=True, choices=DDD_UNITS_CHOICES, help_text=u'Units of defined daily dose')
    ddd_admr = ChemblCharField(max_length=30, blank=True, null=True, help_text=u'Administration route for dose')
    ddd_comment = ChemblCharField(max_length=400, blank=True, null=True, help_text=u'Comment')
    ddd_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Internal primary key')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class MoleculeAtcClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    mol_atc_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key')
    atc_classification = models.ForeignKey(AtcClassification, db_column='level5', help_text=u'ATC code (foreign key to atc_classification table)')
    molecule = models.ForeignKey(MoleculeDictionary, db_column='molregno', help_text=u'Drug to which the ATC code applies (foreign key to molecule_dictionary table)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class Formulations(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    product = models.ForeignKey(Products, help_text=u'Unique identifier of the product. FK to PRODUCTS')
    ingredient = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Name of the approved ingredient within the product')
    strength = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Dose strength')
    record = models.ForeignKey(CompoundRecords, help_text=u'Foreign key to the compound_records table.')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Unique identifier of the ingredient FK to MOLECULE_DICTIONARY')
    formulation_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("record", "product"),  )

#-----------------------------------------------------------------------------------------------------------------------

