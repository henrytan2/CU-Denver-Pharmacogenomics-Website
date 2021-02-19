from django.db import models

# Create your models here.


class DrugNamePrecursorMap(models.Model):
    class Meta:
        managed = True
        db_table = 'drug_name_precursor_map'
    drug_name = models.CharField("drug_name", max_length=100)
    precursor_UUID = models.CharField("precursor_UUID", max_length=36, primary_key=True)
    precursor_DrugID = models.CharField("precursor_DrugID", max_length=12)

