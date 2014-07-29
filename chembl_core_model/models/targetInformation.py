__author__ = 'mnowotka'

import datetime
from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

#-----------------------------------------------------------------------------------------------------------------------

class TargetType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    target_type = ChemblCharField(primary_key=True, max_length=30, help_text=u'Target type (as used in target dictionary)')
    target_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text=u'Description of target type')
    parent_type = ChemblCharField(max_length=25, blank=True, null=True, help_text=u"Higher level classification of target_type, allowing grouping of e.g., all 'PROTEIN' targets, all 'NON-MOLECULAR' targets etc.")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class OrganismClass(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    oc_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Internal primary key')
    tax_id = ChemblPositiveIntegerField(length=11, unique=True, blank=True, null=True, help_text=u'NCBI taxonomy ID for the organism (corresponding to tax_ids in assay2target and target_dictionary tables)')
    l1 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Highest level classification (e.g., Eukaryotes, Bacteria, Fungi etc)')
    l2 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Second level classification')
    l3 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Third level classification')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ProteinFamilyClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    protein_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each classification.')
    protein_class_desc = ChemblCharField(max_length=810, unique=True, help_text=u'Concatenated description of each classification for searching purposes etc.')
    l1 = ChemblCharField(max_length=100, help_text=u'First level classification (e.g., Enzyme, Transporter, Ion Channel).')
    l2 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Second level classification.')
    l3 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Third level classification.')
    l4 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Fourth level classification.')
    l5 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Fifth level classification.')
    l6 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Sixth level classification.')
    l7 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Seventh level classification.')
    l8 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Eighth level classification.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8"),  )

#-----------------------------------------------------------------------------------------------------------------------

class CellDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    cell_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each cell line in the target_dictionary.')
    cell_name = ChemblCharField(max_length=50, help_text=u'Name of each cell line (as used in the target_dicitonary pref_name).')
    cell_description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Longer description (where available) of the cell line.')
    cell_source_tissue = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Tissue from which the cell line is derived, where known.')
    cell_source_organism = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name of organism from which the cell line is derived.')
    cell_source_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID of the organism from which the cell line is derived.') # TODO: should be FK to organism class
    clo_id = ChemblCharField(max_length=11, blank=True, null=True, help_text=u'ID for the corresponding cell line in Cell Line Ontology')
    efo_id = ChemblCharField(max_length=12, blank=True, null=True, help_text=u'ID for the corresponding cell line in Experimental Factory Ontology')
    cellosaurus_id = ChemblCharField(max_length=15, blank=True, null=True, help_text=u'ID for the corresponding cell line in Cellosaurus Ontology')
    downgraded = ChemblPositiveIntegerField(length=1, blank=True, null=True, default=0, help_text=u'Indicates the cell line has been removed (if set to 1)')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("cell_name", "cell_source_tax_id"),  )

#-----------------------------------------------------------------------------------------------------------------------

class ProteinClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    CLASS_LEVEL_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        )

    protein_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each protein family classification.')
    parent_id = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text=u'Protein_class_id for the parent of this protein family.')
    pref_name = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Preferred/full name for this protein family.')
    short_name = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Short/abbreviated name for this protein family (not necessarily unique).')
    protein_class_desc = ChemblCharField(max_length=410, help_text=u'Concatenated description of each classification for searching purposes etc.')
    definition = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'Definition of the protein family.')
    downgraded = ChemblNullableBooleanField()
    replaced_by = ChemblPositiveIntegerField(length=9, blank=True, null=True)
    class_level = ChemblPositiveIntegerField(length=9, blank=True, null=True, choices=CLASS_LEVEL_CHOICES)
    sort_order = ChemblPositiveIntegerField(length=2, blank=True, null=True)
    component_sequences = models.ManyToManyField('ComponentSequences', through="ComponentClass", null=True, blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ComponentSequences(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    COMPONENT_TYPE_CHOICES = (
        ('PROTEIN', 'PROTEIN'),
        ('DNA', 'DNA'),
        ('RNA', 'RNA'),
        )

    DB_SOURCE_CHOICES = (
        ('Manual', 'Manual'),
        ('SWISS-PROT', 'SWISS-PROT'),
        ('TREMBL', 'TREMBL'),
        )

    component_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for the component.')
    component_type = ChemblCharField(max_length=50, blank=True, null=True, choices=COMPONENT_TYPE_CHOICES, help_text=u"Type of molecular component represented (e.g., 'PROTEIN','DNA','RNA').")
    accession = ChemblCharField(max_length=25, unique=True, blank=True, null=True, help_text=u'Accession for the sequence in the source database from which it was taken (e.g., UniProt accession for proteins).')
    sequence = ChemblTextField(blank=True, null=True, help_text=u'A representative sequence for the molecular component, as given in the source sequence database (not necessarily the exact sequence used in the assay).')
    sequence_md5sum = ChemblCharField(max_length=32, blank=True, null=True, help_text=u'MD5 checksum of the sequence.')
    description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Description/name for the molecular component, usually taken from the source sequence database.')
    tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID for the sequence in the source database (i.e., species that the protein/nucleic acid sequence comes from).') # TODO: should be FK to Organism class
    organism = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name of the organism the sequence comes from.')
    db_source = ChemblCharField(max_length=25, blank=True, null=True, choices=DB_SOURCE_CHOICES, help_text=u'The name of the source sequence database from which sequences/accessions are taken. For UniProt proteins, this field indicates whether the sequence is from SWISS-PROT or TREMBL.')
    db_version = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'The version of the source sequence database from which sequences/accession were last updated.')
    insert_date = ChemblDateField(blank=True, null=True, default=datetime.date.today)
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class TargetDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):


    TARGET_PARENT_TYPE_CHOICES = (
        ('MOLECULAR', 'MOLECULAR'),
        ('NON-MOLECULAR', 'NON-MOLECULAR'),
        ('PROTEIN', 'PROTEIN'),
        ('UNDEFINED', 'UNDEFINED'),
        )

    tid = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for the target')
    target_type = models.ForeignKey(TargetType, blank=True, null=True, db_column='target_type', help_text=u'Describes whether target is a protein, an organism, a tissue etc. Foreign key to TARGET_TYPE table.')
    pref_name = ChemblCharField(max_length=200, db_index=True, blank=True, null=True, help_text=u'Preferred target name: manually curated')
    tax_id = ChemblPositiveIntegerField(length=11, db_index=True, blank=True, null=True, help_text=u'NCBI taxonomy id of target') # TODO: should be FK to OrganismClass.tax_id
    organism = ChemblCharField(max_length=150, db_index=True, blank=True, null=True, help_text=u'Source organism of molecuar target or tissue, or the target organism if compound activity is reported in an organism rather than a protein or tissue')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    popularity = ChemblPositiveIntegerField(length=9, blank=True, null=True)
    chembl = models.ForeignKey(ChemblIdLookup, blank=True, null=False, help_text=u'ChEMBL identifier for this target (for use on web interface etc)') # This combination of null and blank is actually very important!
    insert_date = ChemblDateField(blank=True, null=True, default=datetime.date.today)
    target_parent_type = ChemblCharField(max_length=100, blank=True, null=True, choices=TARGET_PARENT_TYPE_CHOICES)
    in_starlite = ChemblNullableBooleanField(default=False)
    species_group_flag = ChemblNullableBooleanField(help_text=u"Flag to indicate whether the target represents a group of species, rather than an individual species (e.g., 'Bacterial DHFR'). Where set to 1, indicates that any associated target components will be a representative, rather than a comprehensive set.")
    downgraded = ChemblNullableBooleanField(default=False)
    component_sequences = models.ManyToManyField('ComponentSequences', through="TargetComponents")
    docs = models.ManyToManyField('Docs', through="Assays")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class ComponentClass(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to component_sequences table.')
    protein_class = models.ForeignKey(ProteinClassification, help_text=u'Foreign key to the protein_classification table.')
    comp_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("component", "protein_class"),  )

#-----------------------------------------------------------------------------------------------------------------------

class ComponentSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    SYN_TYPE_CHOICES = (
        ('HGNC_SYMBOL', 'HGNC_SYMBOL'),
        ('GENE_SYMBOL', 'GENE_SYMBOL'),
        ('UNIPROT', 'UNIPROT'),
        ('MANUAL', 'MANUAL'),
        ('OTHER', 'OTHER'),
        ('EC_NUMBER', 'EC_NUMBER'),
        )

    compsyn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to the component_sequences table. The component to which this synonym applies.')
    component_synonym = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'The synonym for the component.')
    syn_type = ChemblCharField(max_length=20, blank=True, null=True, choices=SYN_TYPE_CHOICES, help_text=u'The type or origin of the synonym (e.g., GENE_SYMBOL).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("component", "component_synonym", "syn_type"),  )

#-----------------------------------------------------------------------------------------------------------------------

class ProteinClassSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    SYN_TYPE_CHOICES = (
        ('CHEMBL', 'CHEMBL'),
        ('CONCEPT_WIKI', 'CONCEPT_WIKI'),
        ('UMLS', 'UMLS'),
        ('CW_XREF', 'CW_XREF'),
        ('MESH_XREF', 'MESH_XREF'),
        )

    protclasssyn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    protein_class = models.ForeignKey(ProteinClassification, help_text=u'Foreign key to the PROTEIN_CLASSIFICATION table. The protein_class to which this synonym applies.')
    protein_class_synonym = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'The synonym for the protein class.')
    syn_type = ChemblCharField(max_length=20, blank=True, null=True, choices=SYN_TYPE_CHOICES, help_text=u'The type or origin of the synonym (e.g., ChEMBL, Concept Wiki, UMLS).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass #unique_together = ( ("protein_class", "protein_class_synonym", "syn_type"),  )

#-----------------------------------------------------------------------------------------------------------------------

class TargetComponents(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    HOMOLOGUE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    RELATIONSHIP_CHOICES = (
        ('COMPARATIVE PROTEIN', 'COMPARATIVE PROTEIN'),
        ('EQUIVALENT PROTEIN', 'EQUIVALENT PROTEIN'),
        ('FUSION PROTEIN', 'FUSION PROTEIN'),
        ('GROUP MEMBER', 'GROUP MEMBER'),
        ('INTERACTING PROTEIN', 'INTERACTING PROTEIN'),
        ('PROTEIN SUBUNIT', 'PROTEIN SUBUNIT'),
        ('RNA', 'RNA'),
        ('RNA SUBUNIT', 'RNA SUBUNIT'),
        ('SINGLE PROTEIN', 'SINGLE PROTEIN'),
        ('UNCURATED', 'UNCURATED'),
        ('SUBUNIT', 'SUBUNIT'),
        )

    STOICHIOMETRY_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (12, '12'),
        )

    target = models.ForeignKey(TargetDictionary, db_column='tid', help_text=u'Foreign key to the target_dictionary, indicating the target to which the components belong.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to the component_sequences table, indicating which components belong to the target.')
    relationship = ChemblCharField(max_length=20, default=u'SUBUNIT', choices=RELATIONSHIP_CHOICES) # TODO: constraint or lookup AND default may be wrong!!!
    stoichiometry = ChemblPositiveIntegerField(length=3, blank=True, null=True, choices=STOICHIOMETRY_CHOICES)
    targcomp_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    homologue = ChemblPositiveIntegerField(length=1, default=0, choices=HOMOLOGUE_CHOICES, help_text=u'Indicates that the given component is a homologue of the correct component (e.g., from a different species) when set to 1. This may be the case if the sequence for the correct protein/nucleic acid cannot be found in sequence databases.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class TargetRelations(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    RELATIONSHIP_CHOICES = (
        ('EQUIVALENT TO', 'EQUIVALENT TO'),
        ('OVERLAPS WITH', 'OVERLAPS WITH'),
        ('SUBSET OF', 'SUBSET OF'),
        ('SUPERSET OF', 'SUPERSET OF'),
        )

    target = models.ForeignKey(TargetDictionary, related_name='to', db_column='tid', help_text=u'Identifier for target of interest (foreign key to target_dictionary table)')
    relationship = ChemblCharField(max_length=20, choices=RELATIONSHIP_CHOICES, help_text=u'Relationship between two targets (e.g., SUBSET OF, SUPERSET OF, OVERLAPS WITH)')
    related_target = models.ForeignKey(TargetDictionary, related_name='from', db_column='related_tid', help_text=u'Identifier for the target that is related to the target of interest (foreign key to target_dicitionary table)')
    targrel_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

