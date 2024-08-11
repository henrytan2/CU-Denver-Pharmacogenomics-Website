from django.db import models

# Create your models here.
class ESNUELOutput(models.Model):

    class Meta:
        managed = False
        db_table = 'esnuel_output'

    id = models.AutoField(primary_key=True)
    smiles_string = models.CharField(max_length=500, unique=True)
    elec_names = models.CharField(max_length=500)
    elec_sites = models.CharField(max_length=500)
    MAAs = models.CharField(max_length=500)
    nuc_names = models.CharField(max_length=500)
    nuc_sites = models.CharField(max_length=500)
    MCAs = models.CharField(max_length=500)