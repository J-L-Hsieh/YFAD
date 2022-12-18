# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DiseaseAll(models.Model):
    disease = models.TextField(db_column='Disease', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Disease_all'


class DiseaseEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    evidencecode = models.TextField(db_column='EvidenceCode', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Disease_evidence'


class GoBpAll(models.Model):
    go_bp = models.TextField(db_column='GO_BP', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GO_BP_all'


class GoBpEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    genedescription = models.TextField(db_column='GeneDescription', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    evidencecode = models.TextField(db_column='EvidenceCode', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GO_BP_evidence'


class GoCcAll(models.Model):
    go_cc = models.TextField(db_column='GO_CC', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GO_CC_all'


class GoCcEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    genedescription = models.TextField(db_column='GeneDescription', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    evidencecode = models.TextField(db_column='EvidenceCode', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GO_CC_evidence'


class GoMfAll(models.Model):
    go_mf = models.TextField(db_column='GO_MF', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GO_MF_all'


class GoMfEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    genedescription = models.TextField(db_column='GeneDescription', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    evidencecode = models.TextField(db_column='EvidenceCode', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GO_MF_evidence'


class Gene(models.Model):
    gene_id = models.TextField(db_column='Gene_id', unique=True)  # Field name made lowercase.
    transcript_id = models.TextField(db_column='transcript_ID', blank=True, null=True)  # Field name made lowercase.
    numbers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gene'


class GeneticInteractionAll(models.Model):
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Genetic_Interaction_all'


class GeneticInteractionEvidence(models.Model):
    systematicname_bait_field = models.TextField(db_column='SystematicName(Bait)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    standardname_bait_field = models.TextField(db_column='StandardName(Bait)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    systematicname_hit_field = models.TextField(db_column='SystematicName(Hit)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    standardname_hit_field = models.TextField(db_column='StandardName(Hit)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    experimenttype = models.TextField(db_column='ExperimentType', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    bait_link = models.TextField(db_column='Bait_link', blank=True, null=True)  # Field name made lowercase.
    hit_link = models.TextField(db_column='Hit_link', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Genetic_Interaction_evidence'


class MutantPhenotypeAll(models.Model):
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mutant_Phenotype_all'


class MutantPhenotypeEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mutant_Phenotype_evidence'


class PathwayAll(models.Model):
    pathway = models.TextField(db_column='Pathway', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pathway_all'


class PathwayEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pathway_evidence'


class PhysicalInteractionAll(models.Model):
    physical_interaction = models.TextField(db_column='Physical_Interaction', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Physical_Interaction_all'


class PhysicalInteractionEvidence(models.Model):
    systematicname_bait_field = models.TextField(db_column='SystematicName(Bait)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    standardname_bait_field = models.TextField(db_column='StandardName(Bait)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    systematicname_hit_field = models.TextField(db_column='SystematicName(Hit)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    standardname_hit_field = models.TextField(db_column='StandardName(Hit)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    experimenttype = models.TextField(db_column='ExperimentType', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    bait_link = models.TextField(db_column='Bait_link', blank=True, null=True)  # Field name made lowercase.
    hit_link = models.TextField(db_column='Hit_link', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Physical_Interaction_evidence'


class ProteinDomainAll(models.Model):
    protein_domain = models.TextField(db_column='Protein_Domain', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Protein_Domain_all'


class ProteinDomainEvidence(models.Model):
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.
    domaindescription = models.TextField(db_column='DomainDescription', blank=True, null=True)  # Field name made lowercase.
    startcoordinate = models.IntegerField(db_column='StartCoordinate', blank=True, null=True)  # Field name made lowercase.
    endcoordinate = models.IntegerField(db_column='EndCoordinate', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Protein_Domain_evidence'


class TranscriptionalRegulationAll(models.Model):
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', unique=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    disease = models.TextField(db_column='Disease', blank=True, null=True)  # Field name made lowercase.
    genetic_interaction = models.TextField(db_column='Genetic_Interaction', blank=True, null=True)  # Field name made lowercase.
    go_cc = models.TextField(db_column='GO_CC', blank=True, null=True)  # Field name made lowercase.
    go_mf = models.TextField(db_column='GO_MF', blank=True, null=True)  # Field name made lowercase.
    go_bp = models.TextField(db_column='GO_BP', blank=True, null=True)  # Field name made lowercase.
    pathway = models.TextField(db_column='Pathway', blank=True, null=True)  # Field name made lowercase.
    mutant_phenotype = models.TextField(db_column='Mutant_Phenotype', blank=True, null=True)  # Field name made lowercase.
    physical_interaction = models.TextField(db_column='Physical_Interaction', blank=True, null=True)  # Field name made lowercase.
    protein_domain = models.TextField(db_column='Protein_Domain', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transcriptional_Regulation_all'


class TranscriptionalRegulationEvidence(models.Model):
    regulator = models.TextField(blank=True, null=True)
    systematicname = models.TextField(db_column='SystematicName', blank=True, null=True)  # Field name made lowercase.
    standardname = models.TextField(db_column='StandardName', blank=True, null=True)  # Field name made lowercase.
    transcriptional_regulation = models.TextField(db_column='Transcriptional_Regulation', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    term_link = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Transcriptional_Regulation_evidence'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TranscriptWbidType(models.Model):
    index = models.IntegerField()
    transcript = models.TextField(blank=True, null=True)
    wormbase_id = models.TextField(db_column='Wormbase_id', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transcript_wbid_type'


class WebToolGene(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    gene_id = models.CharField(max_length=100)
    transcript_id = models.CharField(max_length=100)
    numbers = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'web_tool_gene'


class WebToolUser(models.Model):
    user_name = models.CharField(primary_key=True, max_length=100)
    user_password = models.CharField(max_length=100)
    user_content = models.TextField()

    class Meta:
        managed = False
        db_table = 'web_tool_user'


class Wormbase(models.Model):
    wormbase_id = models.TextField(db_column='WormBase ID', unique=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    sequence_name = models.TextField(db_column='Sequence Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gene_name = models.TextField(db_column='Gene Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_name = models.TextField(db_column='Other Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'wormbase'


class WormbaseGenetranscriptW285(models.Model):
    wormbase_id = models.TextField(db_column='WormBase_ID', unique=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    sequence_name = models.TextField(db_column='Sequence_Name', blank=True, null=True)  # Field name made lowercase.
    gene_name = models.TextField(db_column='Gene_Name', blank=True, null=True)  # Field name made lowercase.
    other_name = models.TextField(db_column='Other_Name', blank=True, null=True)  # Field name made lowercase.
    transcript = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    transcript_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wormbase_genetranscript W285'
