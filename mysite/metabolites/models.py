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
    metab_ID = models.CharField("MetaboliteID", max_length=10)
    reaction = models.CharField("Reaction", max_length=45)
    reaction_ID = models.CharField("ReactionID", max_length=10, unique=True)
    enzyme = models.CharField("Enzyme", max_length=45)
    biosystem = models.CharField("Biosystem", max_length=45)
    precursor_smiles = models.CharField("PrecursorSmiles", max_length=250)
    precursor_InChi = models.CharField("PrecursorInchi", max_length=400, unique=True)
    precursor_InChiKey = models.CharField("PrecursorInchiKey", max_length=27)
    logp = models.DecimalField("logp", max_digits=22, decimal_places=20, default=None)
    max_rmsd = models.DecimalField("max_rmsd", max_digits=22, decimal_places=20, default=None)
    biotrans_origin = models.CharField("biotrans_origin", max_length=20, default=None)


