__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

#-----------------------------------------------------------------------------------------------------------------------

class ActionType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    action_type = ChemblCharField(primary_key=True, max_length=50, help_text=u'Primary key. Type of action of the drug e.g., agonist, antagonist')
    description = ChemblCharField(max_length=200, help_text=u'Description of how the action type is used')
    parent_type = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Higher-level grouping of action types e.g., positive vs negative action')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class DrugMechanism(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):


    CURATION_STATUS_CHOICES = (
        ('COMPLETE', 'COMPLETE'),
        ('PARTIAL', 'PARTIAL'),
        )

    SELECTIVITY_COMMENT_CHOICES = (
        ('Broad spectrum', 'Broad spectrum'),
        ('EDG5 less relevant', 'EDG5 less relevant'),
        ('M3 selective', 'M3 selective'),
        ("Non-selective but type 5 receptor is overexpressed in Cushing's disease", "Non-selective but type 5 receptor is overexpressed in Cushing's disease"),
        ('Selective', 'Selective'),
        ('Selective for the brain omega-1 receptor (i.e. BZ1-type, i.e. alpha1/beta1/gamma2-GABA receptor)', 'Selective for the brain omega-1 receptor (i.e. BZ1-type, i.e. alpha1/beta1/gamma2-GABA receptor)'),
        ('Selectivity for types 2, 3 and 5', 'Selectivity for types 2, 3 and 5'),
        ('selectivity for beta-3 containing complexes', 'selectivity for beta-3 containing complexes'),
        )

    mec_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key for each drug mechanism of action')
    record = models.ForeignKey(CompoundRecords, help_text=u'Record_id for the drug (foreign key to compound_records table)')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Molregno for the drug (foreign key to molecule_dictionary table)')
    mechanism_of_action = ChemblCharField(max_length=250, blank=True, null=True, help_text=u"Description of the mechanism of action e.g., 'Phosphodiesterase 5 inhibitor'")
    target = models.ForeignKey(TargetDictionary, blank=True, null=True, db_column='tid', help_text=u'Target associated with this mechanism of action (foreign key to target_dictionary table)')
    site = models.ForeignKey(BindingSites, blank=True, null=True, help_text=u'Binding site for the drug within the target (where known) - foreign key to binding_sites table')
    action_type = models.ForeignKey(ActionType, blank=True, null=True, db_column='action_type', help_text=u'Type of action of the drug on the target e.g., agonist/antagonist etc (foreign key to action_type table)')
    direct_interaction = ChemblNullableBooleanField(help_text=u'Flag to show whether the molecule is believed to interact directly with the target (1 = yes, 0 = no)')
    molecular_mechanism = ChemblNullableBooleanField(help_text=u'Flag to show whether the mechanism of action describes the molecular target of the drug, rather than a higher-level physiological mechanism e.g., vasodilator (1 = yes, 0 = no)')
    disease_efficacy = ChemblNullableBooleanField(help_text=u'Flag to show whether the target assigned is believed to play a role in the efficacy of the drug in the indication(s) for which it is approved (1 = yes, 0 = no)')
    mechanism_comment = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Additional comments regarding the mechanism of action')
    selectivity_comment = ChemblCharField(max_length=100, blank=True, null=True, choices=SELECTIVITY_COMMENT_CHOICES, help_text=u'Additional comments regarding the selectivity of the drug')
    binding_site_comment = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Additional comments regarding the binding site of the drug')
    curated_by = ChemblCharField(max_length=20, blank=True, null=True)
    date_added = ChemblDateField(blank=True, null=True, default=datetime.date.today)
    date_removed = ChemblDateField(blank=True, null=True)
    downgraded = ChemblNullableBooleanField()
    downgrade_reason = ChemblCharField(max_length=200, blank=True, null=True)
    uniprot_accessions = ChemblCharField(max_length=500, blank=True, null=True)
    curator_comment = ChemblCharField(max_length=500, blank=True, null=True)
    curation_status = ChemblCharField(max_length=10, default=u'PARTIAL', choices=CURATION_STATUS_CHOICES, help_text=u'Show whether the curation for this row is complete')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class LigandEff(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    activity = models.OneToOneField(Activities, primary_key=True, help_text=u'Link key to activities table')
    bei = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Binding Efficiency Index = p(XC50) *1000/MW_freebase')
    sei = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Surface Efficiency Index = p(XC50)*100/PSA')
    le = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Ligand Efficiency = deltaG/heavy_atoms  [from the Hopkins DDT paper 2004]')
    lle = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Lipophilic Ligand Efficiency = -logKi-ALogP. [from Leeson NRDD 2007]')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class PredictedBindingDomains(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    CONFIDENCE_CHOICES = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low', 'low'),
        )

    PREDICTION_METHOD_CHOICES = (
        ('Manual', 'Manual'),
        ('Multi domain', 'Multi domain'),
        ('Single domain', 'Single domain'),
        )

    predbind_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    activity = models.ForeignKey(Activities, blank=True, null=True, help_text=u'Foreign key to the activities table, indicating the compound/assay(+target) combination for which this prediction is made.')
    site = models.ForeignKey(BindingSites, blank=True, null=True, help_text=u'Foreign key to the binding_sites table, indicating the binding site (domain) that the compound is predicted to bind to.')
    prediction_method = ChemblCharField(max_length=50, blank=True, null=True, choices=PREDICTION_METHOD_CHOICES, help_text=u"The method used to assign the binding domain (e.g., 'Single domain' where the protein has only 1 domain, 'Multi domain' where the protein has multiple domains, but only 1 is known to bind small molecules in other proteins).") # TODO: constraint should be added
    confidence = ChemblCharField(max_length=10, blank=True, null=True, choices=CONFIDENCE_CHOICES, help_text=u'The level of confidence assigned to the prediction (high where the protein has only 1 domain, medium where the compound has multiple domains, but only 1 known small molecule-binding domain).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

#-----------------------------------------------------------------------------------------------------------------------

class MechanismRefs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):


    REF_TYPE_CHOICES = (
        ('ISBN', 'ISBN'),
        ('IUPHAR', 'IUPHAR'),
        ('DOI', 'DOI'),
        ('EMA', 'EMA'),
        ('PubMed', 'PUBMED'),
        ('USPO', 'USPO'),
        ('DailyMed', 'DAILYMED'),
        ('FDA', 'FDA'),
        ('Expert', 'EXPERT'),
        ('Other', 'OTHER'),
        ('InterPro', 'INTERPRO'),
        ('Wikipedia', 'WIKIPEDIA'),
        ('UniProt', 'UNIPROT'),
        ('KEGG', 'KEGG'),
        )

    mecref_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key')
    mechanism = models.ForeignKey(DrugMechanism, db_column='mec_id', help_text=u'Foreign key to drug_mechanism table - indicating the mechanism to which the references refer')
    ref_type = ChemblCharField(max_length=50, choices=REF_TYPE_CHOICES, help_text=u"Type/source of reference (e.g., 'PubMed','DailyMed')")
    ref_id = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)')
    ref_url = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Full URL linking to the reference')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("mechanism", "ref_type", "ref_id"),  )

#-----------------------------------------------------------------------------------------------------------------------

