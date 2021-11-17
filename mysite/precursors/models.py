from django.db import models


class Precursors(models.Model):
    class Meta:
        managed = True
        db_table = 'precursors'

    UUID = models.CharField("UUID", max_length=36, primary_key=True)
    DrugID = models.CharField("DrugID", max_length=100)
    DrugName = models.CharField("DrugName", max_length=100, null=False)
    SmileCode = models.CharField("SmileCode", max_length=255, null=False)
    InChiKey = models.CharField("InChiKey", max_length=100, null=False)
    logp = models.DecimalField("logp", max_digits=22, decimal_places=20)
    max_rmsd = models.DecimalField("max_rmsd", max_digits=22, decimal_places=20)
