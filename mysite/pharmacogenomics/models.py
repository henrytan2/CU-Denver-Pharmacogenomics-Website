from django.db import models

# Create your models here.


class SideEffect(models.Model):
    drug_id = models.CharField('Drug ID', max_length=100)
    stereoisomer = models.CharField('Stereoisomer ID', max_length=100)
    umls_concept_id = models.CharField('UMLS Concept ID', max_length=100)
    frequency_percent = models.CharField('Frequency(%)', max_length=20)
    frequency_lower = models.CharField('Frequency Lower', max_length=100)
    frequency_upper = models.CharField('Frequency Upper', max_length=100)
    concept_type = models.CharField('Concept Type', max_length=5)
    side_effect = models.CharField('Side Effect', max_length=100)
    drug_name = models.CharField('Drug Name', max_length=100)
    atc_code = models.CharField('ATC Code', max_length=10)

    def __str__(self):
        return self.drug_id

class Drugs_List(models.Model):
    drug_id = models.CharField('Drug ID', max_length=100)
    stereoisomer = models.CharField('Stereoisomer ID', max_length=100)
    umls_concept_id = models.CharField('UMLS Concept ID', max_length=100)
    frequency_percent = models.CharField('Frequency(%)', max_length=20)
    frequency_lower = models.CharField('Frequency Lower', max_length=100)
    frequency_upper = models.CharField('Frequency Upper', max_length=100)
    concept_type = models.CharField('Concept Type', max_length=5)
    side_effect = models.CharField('Side Effect', max_length=100)
    drug_name = models.CharField('Drug Name', max_length=100)
    atc_code = models.CharField('ATC Code', max_length=10)

    def __str__(self):
        return self.drug_id
