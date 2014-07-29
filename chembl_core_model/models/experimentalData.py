__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

#-----------------------------------------------------------------------------------------------------------------------

class AssayType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    assay_type = ChemblCharField(primary_key=True, max_length=1, help_text=u'Single character representing assay type')
    assay_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text=u'Description of assay type')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class RelationshipType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    relationship_type = ChemblCharField(primary_key=True, max_length=1, help_text=u'Relationship_type flag used in the assay2target table')
    relationship_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text=u'Description of relationship_type flags')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ConfidenceScoreLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    confidence_score = ChemblPositiveIntegerField(primary_key=True, length=1, help_text=u'0-9 score showing level of confidence in assignment of the precise molecular target of the assay')
    description = ChemblCharField(max_length=100, help_text=u'Description of the target types assigned with each score')
    target_mapping = ChemblCharField(max_length=30, help_text=u'Short description of the target types assigned with each score')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class CurationLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    curated_by = ChemblCharField(primary_key=True, max_length=32, help_text=u'Short description of the level of curation')
    description = ChemblCharField(max_length=100, help_text=u'Definition of terms in the curated_by field.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ActivityStdsLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    std_act_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    standard_type = ChemblCharField(max_length=250, help_text=u'The standard_type that other published_types in the activities table have been converted to.')
    definition = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'A description/definition of the standard_type.')
    standard_units = ChemblCharField(max_length=100, help_text=u'The units that are applied to this standard_type and to which other published_units are converted. Note a standard_type may have more than one allowable standard_unit and therefore multiple rows in this table.')
    normal_range_min = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=12, help_text=u"The lowest value for this activity type that is likely to be genuine. This is only an approximation, so lower genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table below this threshold are flagged with a data_validity_comment of 'Outside typical range'.")
    normal_range_max = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=12, help_text=u"The highest value for this activity type that is likely to be genuine. This is only an approximation, so higher genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table above this threshold are flagged with a data_validity_comment of 'Outside typical range'.")

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("standard_type", "standard_units"),  )

#-----------------------------------------------------------------------------------------------------------------------

class DataValidityLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    data_validity_comment = ChemblCharField(primary_key=True, max_length=30, help_text=u'Primary key. Short description of various types of errors/warnings applied to values in the activities table.')
    description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Definition of the terms in the data_validity_comment field.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ParameterType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):


    parameter_type = ChemblCharField(primary_key=True, max_length=20, help_text=u'Short name for the type of parameter associated with an assay')
    description = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'Description of the parameter type')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class Assays(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ASSAY_CATEGORY_CHOICES = (
        ('screening', 'screening'),
        ('panel', 'panel'),
        ('confirmatory', 'confirmatory'),
        ('summary', 'summary'),
        ('other', 'other'),
        )

    ASSAY_TEST_TYPE_CHOICES = (
        ('In vivo', 'In vivo'),
        ('In vitro', 'In vitro'),
        ('Ex vivo', 'Ex vivo'),
        )

    assay_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for the assay')
    doc = models.ForeignKey(Docs, help_text=u'Foreign key to documents table')
    description = ChemblCharField(max_length=4000, db_index=True, blank=True, null=True, help_text=u'Description of the reported assay')
    assay_type = models.ForeignKey(AssayType, blank=True, null=True, db_column='assay_type', help_text=u'Assay classification, e.g. B=Binding assay, A=ADME assay, F=Functional assay')
    assay_test_type = ChemblCharField(max_length=20, blank=True, null=True, choices=ASSAY_TEST_TYPE_CHOICES, help_text=u'Type of assay system (i.e., in vivo or in vitro)')
    assay_category = ChemblCharField(max_length=20, blank=True, null=True, choices=ASSAY_CATEGORY_CHOICES, help_text=u'screening, confirmatory (ie: dose-response), summary, panel or other.')
    assay_organism = ChemblCharField(max_length=250, blank=True, null=True, help_text=u'Name of the organism for the assay system (e.g., the organism, tissue or cell line in which an assay was performed). May differ from the target organism (e.g., for a human protein expressed in non-human cells, or pathogen-infected human cells).')
    assay_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID for the assay organism.')  # TODO: should be FK to OrganismClass.tax_id
    assay_strain = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Name of specific strain of the assay organism used (where known)')
    assay_tissue = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Name of tissue used in the assay system (e.g., for tissue-based assays) or from which the assay system was derived (e.g., for cell/subcellular fraction-based assays).')
    assay_cell_type = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Name of cell type or cell line used in the assay system (e.g., for cell-based assays).')
    assay_subcellular_fraction = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Name of subcellular fraction used in the assay system (e.g., microsomes, mitochondria).')
    target = models.ForeignKey(TargetDictionary, blank=True, null=True, db_column='tid', help_text=u'Target identifier to which this assay has been mapped. Foreign key to target_dictionary. From ChEMBL_15 onwards, an assay will have only a single target assigned.')
    relationship_type = models.ForeignKey(RelationshipType, blank=True, null=True, db_column='relationship_type', help_text=u'Flag indicating of the relationship between the reported target in the source document and the assigned target from TARGET_DICTIONARY. Foreign key to RELATIONSHIP_TYPE table.')
    confidence_score = models.ForeignKey(ConfidenceScoreLookup, blank=True, null=True, db_column='confidence_score', help_text=u'Confidence score, indicating how accurately the assigned target(s) represents the actually assay target. Foreign key to CONFIDENCE_SCORE table. 0 means uncurated/unassigned, 1 = low confidence to 9 = high confidence.')
    curated_by = models.ForeignKey(CurationLookup, blank=True, null=True, db_column='curated_by', help_text=u'Indicates the level of curation of the target assignment. Foreign key to curation_lookup table.')
    activity_count = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text=u'Number of activities recorded for this assay')
    assay_source = ChemblCharField(max_length=50, db_index=True, blank=True, null=True)
    src = models.ForeignKey(Source, help_text=u'Foreign key to source table')
    src_assay_id = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Identifier for the assay in the source database/deposition (e.g., pubchem AID)')
    chembl = models.ForeignKey(ChemblIdLookup, unique=True, help_text=u'ChEMBL identifier for this assay (for use on web interface etc)')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=250, blank=True, null=True)
    orig_description = ChemblCharField(max_length=4000, blank=True, null=True)
    a2t_complex = ChemblNullableBooleanField()
    a2t_multi = ChemblNullableBooleanField()
    mc_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True)
    mc_organism = ChemblCharField(max_length=100, blank=True, null=True)
    mc_target_type = ChemblCharField(max_length=25, blank=True, null=True)
    mc_target_name = ChemblCharField(max_length=4000, blank=True, null=True)
    mc_target_accession = ChemblCharField(max_length=255, blank=True, null=True)
    a2t_assay_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True)
    a2t_assay_organism = ChemblCharField(max_length=250, blank=True, null=True)
    a2t_updated_on = ChemblDateField(blank=True, null=True)
    a2t_updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    cell = models.ForeignKey(CellDictionary, blank=True, null=True, help_text=u'Foreign key to cell dictionary. The cell type or cell line used in the assay')
    bao_format = ChemblCharField(max_length=11, db_index=True, blank=True, null=True, help_text=u'ID for the corresponding format type in BioAssay Ontology (e.g., cell-based, biochemical, organism-based etc)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class Activities(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    MANUAL_CURATION_FLAG_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    STANDARD_RELATION_CHOICES = (
        ('>', '>'),
        ('<', '<'),
        ('=', '='),
        ('~', '~'),
        ('<=', '<='),
        ('>=', '>='),
        ('<<', '<<'),
        ('>>', '>>'),
        )

    activity_id = ChemblAutoField(primary_key=True, length=11, help_text=u'Unique ID for the activity row')
    assay = models.ForeignKey(Assays, help_text=u'Foreign key to the assays table (containing the assay description)')
    doc = models.ForeignKey(Docs, blank=True, null=True, help_text=u'Foreign key to documents table (for quick lookup of publication details - can also link to documents through compound_records or assays table)')
    record = models.ForeignKey(CompoundRecords, help_text=u'Foreign key to the compound_records table (containing information on the compound tested)')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Foreign key to compounds table (for quick lookup of compound structure - can also link to compounds through compound_records table)')
    activity_type = ChemblCharField(max_length=250, db_index=True, blank=True, null=True, help_text=u'Deprecated. Use published_activity_type or standard_type columns') # TODO: Deprecated
    standard_relation = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, novalidate=True, choices=STANDARD_RELATION_CHOICES, help_text=u'Symbol constraining the activity value (e.g. >, <, =)')
    published_value = ChemblNoLimitDecimalField(db_index=True, blank=True, null=True, help_text=u'Datapoint value as it appears in the original publication.') # TODO: NUMBER in Oracle
    published_units = ChemblCharField(max_length=100, db_index=True, blank=True, null=True, help_text=u'Units of measurement as they appear in the original publication')
    standard_value = ChemblNoLimitDecimalField(db_index=True, blank=True, null=True, help_text=u'Same as PUBLISHED_VALUE but transformed to common units: e.g. mM concentrations converted to nM.') # TODO: NUMBER in Oracle
    standard_units = ChemblCharField(max_length=100, db_index=True, blank=True, null=True, help_text=u"Selected 'Standard' units for data type: e.g. concentrations are in nM.")
    standard_flag = ChemblNullableBooleanField(help_text=u'Shows whether the standardised columns have been curated/set (1) or just default to the published data (0).')
    standard_type = ChemblCharField(max_length=250, db_index=True, blank=True, null=True, help_text=u'Standardised version of the published_activity_type (e.g. IC50 rather than Ic-50/Ic50/ic50/ic-50)')
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    updated_on = ChemblDateField(blank=True, null=True)
    activity_comment = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u"Describes non-numeric activities i.e. 'Slighty active', 'Not determined'")
    published_type = ChemblCharField(max_length=250, db_index=True, blank=True, null=True, help_text=u'Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original publication')
    manual_curation_flag = ChemblPositiveIntegerField(length=1, blank=True, null=True, default=0, choices=MANUAL_CURATION_FLAG_CHOICES)
    data_validity_comment = models.ForeignKey(DataValidityLookup, blank=True, null=True, db_column='data_validity_comment', help_text=u"Comment reflecting whether the values for this activity measurement are likely to be correct - one of 'Manually validated' (checked original paper and value is correct), 'Potential author error' (value looks incorrect but is as reported in the original paper), 'Outside typical range' (value seems too high/low to be correct e.g., negative IC50 value), 'Non standard unit type' (units look incorrect for this activity type).")
    potential_duplicate = ChemblNullableBooleanField(help_text=u'Indicates whether the value is likely to be a repeat citation of a value reported in a previous ChEMBL paper, rather than a new, independent measurement.') # TODO: this has only two states: (null, 1), change it to (0,1)
    published_relation = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Symbol constraining the activity value (e.g. >, <, =), as it appears in the original publication')
    original_activity_id = ChemblPositiveIntegerField(length=11, blank=True, null=True) # TODO: should that be FK referencing Activities in future?
    pchembl_value = models.DecimalField(db_index=True, blank=True, null=True, max_digits=4, decimal_places=2, help_text=u'Negative log of selected concentration-response activity values (IC50/EC50/XC50/AC50/Ki/Kd/Potency)')
    bao_endpoint = ChemblCharField(max_length=11, blank=True, null=True, help_text=u'ID for the corresponding result type in BioAssay Ontology (based on standard_type)')
    uo_units = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'ID for the corresponding unit in Unit Ontology (based on standard_units)')
    qudt_units = ChemblCharField(max_length=70, blank=True, null=True, help_text=u'ID for the corresponding unit in QUDT Ontology (based on standard_units)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class AssayParameters(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    assay_param_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Numeric primary key')
    assay = models.ForeignKey(Assays, help_text=u'Foreign key to assays table. The assay to which this parameter belongs')
    parameter_type = models.ForeignKey(ParameterType, db_column='parameter_type', help_text=u'Foreign key to parameter_type table, defining the meaning of the parameter')
    parameter_value = ChemblCharField(max_length=2000, help_text=u'The value of the particular parameter')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("assay", "parameter_type"),  )

#-----------------------------------------------------------------------------------------------------------------------

