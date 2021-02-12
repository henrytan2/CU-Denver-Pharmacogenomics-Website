from django.db import models

# Create your models here.
class PrecursorMetaboliteMap(models.Model):
    class Meta:
        managed = True
        db_table = 'precursor_metabolite_map'

    precursor_UUID = models.CharField("precursor_UUID", max_length=36, null=False)
    metabolite_UUID = models.CharField("metabolite_UUID", primary_key=True, max_length=36, null=False)
    origin = models.CharField("origin", max_length=12, null=False)
