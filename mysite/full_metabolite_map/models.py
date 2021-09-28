from django.db import models


class FullMetaboliteMap(models.Model):
    class Meta:
        managed = True
        db_table = 'full_metabolite_map'

    UUID = models.CharField("UUID", max_length=36, primary_key=True)
    precursor_UUID = models.CharField("UUID", max_length=36)
    metabolite_UUID = models.CharField("UUID", max_length=36)
    origin = models.CharField("origin", max_length=12, null=False)
    level = models.IntegerField("level", null=False)
