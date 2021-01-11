from django.db import models


# Create your models here.
class Metabolite(models.Model):
    class Meta:
        managed = True
        db_table = 'metabolites'

    UUID = models.CharField("UUID", max_length=36, primary_key=True)
    metabolite_InChi = models.CharField("MetaboliteInchi", max_length=4000)
    metabolite_InChiKey = models.CharField("MetaboliteInchiKey", max_length=27, unique=True)
    metabolite_smile_string = models.CharField("MetaboliteSmileString", max_length=250)
    metab_ID = models.CharField("MetaboliteID", max_length=100)
    reaction = models.CharField("Reaction", max_length=100)
    reaction_ID = models.CharField("ReactionID", max_length=100)
    enzyme = models.CharField("Enzyme", max_length=200)
    biosystem = models.CharField("Biosystem", max_length=88)
    precursor_smiles = models.CharField("PrecursorSmiles", max_length=1000)
    precursor_InChi = models.CharField("PrecursorInchi", max_length=2000)
    precursor_InChiKey = models.CharField("PrecursorInchiKey", max_length=280)
    biotrans_origin = models.CharField("BiotransformerOrigin", max_length=88)
    logp = models.CharField("logp", max_length=21)
    max_rmsd = models.CharField("MaxRMSD", max_length=21)
