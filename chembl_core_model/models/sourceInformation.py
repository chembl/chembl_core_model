__author__ = 'mnowotka'

from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

#-----------------------------------------------------------------------------------------------------------------------

class Source(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    src_id = ChemblAutoField(primary_key=True, length=3, help_text=u'Identifier for each source (used in compound_records and assays tables)')
    src_description = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Description of the data source')
    src_short_name = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'A short name for each data source, for display purposes')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class Journals(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    journal_id = ChemblAutoField(primary_key=True, length=9)
    title = ChemblCharField(max_length=100, blank=True, null=True)
    iso_abbreviation = ChemblCharField(max_length=50, blank=True, null=True)
    issn_print = ChemblCharField(max_length=20, blank=True, null=True)
    issn_electronic = ChemblCharField(max_length=20, blank=True, null=True)
    publication_start_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    nlm_id = ChemblCharField(max_length=15, blank=True, null=True)
    doc_journal = ChemblCharField(max_length=50, blank=True, null=True)
    core_journal_flag = ChemblNullableBooleanField()

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class Docs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    DOC_TYPE_CHOICES = (
        ('PUBLICATION', 'PUBLICATION'),
        ('BOOK', 'BOOK'),
        ('DATASET', 'DATASET'),
        )

    doc_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for the document')
    journal = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Abbreviated journal name for an article')
    year = ChemblPositiveIntegerField(length=4, db_index=True, blank=True, null=True, help_text=u'Year of journal article publication') # TODO: should be date!
    volume = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Volume of journal article')
    issue = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Issue of journal article')
    first_page = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'First page number of journal article')
    last_page = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Last page number of journal article')
    pubmed_id = ChemblPositiveIntegerField(length=11, unique=True, blank=True, null=True, help_text=u'NIH pubmed record ID, where available')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    doi = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Digital object identifier for this reference')
    chembl = models.ForeignKey(ChemblIdLookup, unique=True, blank=True, null=False, help_text=u'ChEMBL identifier for this document (for use on web interface etc)') # This combination of null and blank is actually very important!
    title = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Document title (e.g., Publication title or description of dataset)')
    doc_type = ChemblCharField(max_length=50, choices=DOC_TYPE_CHOICES, help_text=u'Type of the document (e.g., Publication, Deposited dataset)')
    authors = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'For a deposited dataset, the authors carrying out the screening and/or submitting the dataset.')
    abstract = ChemblTextField(blank=True, null=True, help_text=u'For a deposited dataset, a brief description of the dataset.')
    journal_id = models.ForeignKey(Journals, blank=True, null=True, db_column='journal_id')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class JournalArticles(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    int_pk = ChemblAutoField(primary_key=True, length=9)
    journal = models.ForeignKey(Journals)
    volume = ChemblPositiveIntegerField(length=5, db_index=True, blank=True, null=True)
    issue = ChemblPositiveIntegerField(length=5, db_index=True, blank=True, null=True)
    year = ChemblPositiveIntegerField(length=4, db_index=True, blank=True, null=True)
    month = ChemblPositiveIntegerField(length=2, db_index=True, blank=True, null=True)
    day = ChemblPositiveIntegerField(length=2, db_index=True, blank=True, null=True)
    pagination = ChemblCharField(max_length=50, db_index=True, blank=True, null=True)
    first_page = ChemblCharField(max_length=50, db_index=True, blank=True, null=True)
    last_page = ChemblCharField(max_length=50, db_index=True, blank=True, null=True)
    pubmed_id = ChemblPositiveIntegerField(length=11, db_index=True, blank=True, null=True)
    doi = ChemblCharField(max_length=50, blank=True, null=True)
    title = ChemblTextField(blank=True, null=True)
    abstract = ChemblTextField(blank=True, null=True)
    authors = ChemblTextField(blank=True, null=True)
    year_raw = ChemblCharField(max_length=50, blank=True, null=True)
    month_raw = ChemblCharField(max_length=50, blank=True, null=True)
    day_raw = ChemblCharField(max_length=50, blank=True, null=True)
    volume_raw = ChemblCharField(max_length=50, blank=True, null=True)
    issue_raw = ChemblCharField(max_length=50, blank=True, null=True)
    date_loaded = ChemblDateField(blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

