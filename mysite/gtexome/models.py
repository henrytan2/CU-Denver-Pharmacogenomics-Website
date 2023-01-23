from django.db import models


class GTEx(models.Model):
    class Meta:
        managed = True
        db_table = 'gtexome_gtex'

    gene_id = models.CharField('Gene ID', max_length=20)
    description = models.CharField('Description', max_length=20)
    adipose_subcutaneous = models.FloatField('Adipose-Subcutaneous', max_length=10)
    adipose_visceral_omentum = models.FloatField('Adipose-Visceral(Omentum)', max_length=10)
    adrenal_gland = models.FloatField('Adrenal-Gland', max_length=10)
    artery_aorta = models.FloatField('Artery-Aorta', max_length=10)
    artery_coronary = models.FloatField('Artery-Coronary', max_length=10)
    artery_tibial = models.FloatField('Artery-Tibial', max_length=10)
    bladder = models.FloatField('Bladder', max_length=10)
    brain_amygdala = models.FloatField('Brain-Amygdala', max_length=10)
    brain_anterior_cingulate_cortex_BA24 = models.FloatField('Brain-Anterior-cingulate-cortex-(BA24)', max_length=10)
    brain_caudate_basalganglia = models.FloatField('Brain-Caudate(basalganglia)', max_length=10)
    brain_cerebral_hemisphere = models.FloatField('Brain-CerebellarHemisphere', max_length=10)
    brain_cerebellum = models.FloatField('Brain-Cerebellum', max_length=10)
    brain_cortex = models.FloatField('Brain-Cortex', max_length=10)
    brain_frontal_cortex_BA9 = models.FloatField('Brain-FrontalCortex(BA9)', max_length=10)
    brain_hippocampus = models.FloatField('Brain-Hippocampus', max_length=10)
    brain_hypothalamus = models.FloatField('Brain-Hypothalamus', max_length=10)
    brain_nucleusaccumbens_basalganglia = models.FloatField('Brain-Nucleusaccumbens(basalganglia)', max_length=10)
    brain_putamen_basalganglia = models.FloatField('Brain-Putamen(basalganglia)', max_length=10)
    brain_spinalcord_cervicalc_1 = models.FloatField('Brain-Spinalcord(cervicalc-1)', max_length=10)
    brain_substantianigra = models.FloatField('Brain-Substantianigra', max_length=10)
    breast_mammary_tissue = models.FloatField('Breast-MammaryTissue', max_length=10)
    cells_cultured_fibroblasts = models.FloatField('Cells-Cultured-fibroblasts', max_length=10)
    cells_ebv_transformed_lymphocytes = models.FloatField('Cells-EBV-transformedlymphocytes', max_length=10)
    cervix_ectocervix = models.FloatField('Cervix-Ectocervix', max_length=10)
    cervix_endocervix = models.FloatField('Cervix-Endocervix', max_length=10)
    colon_sigmoid = models.FloatField('Colon-Sigmoid', max_length=10)
    colon_transverse = models.FloatField('Colon-Transverse', max_length=10)
    esophagus_gastroesophageal_junction = models.FloatField('Esophagus-GastroesophagealJunction', max_length=10)
    esophagus_mucosa = models.FloatField('Esophagus-Mucosa', max_length=10)
    esophagus_muscularis = models.FloatField('Esophagus-Muscularis', max_length=10)
    fallopian_tube = models.FloatField('FallopianTube', max_length=10)
    heart_atrial_appendage = models.FloatField('Heart-AtrialAppendage', max_length=10)
    heart_left_ventricle = models.FloatField('Heart-LeftVentricle', max_length=10)
    kidney_cortex = models.FloatField('Kidney-Cortex', max_length=10)
    kidney_medulla = models.FloatField('Kidney-Medulla', max_length=10)
    liver = models.FloatField('Liver', max_length=10)
    lung = models.FloatField('Lung', max_length=10)
    minor_salivary_gland = models.FloatField('MinorSalivaryGland', max_length=10)
    muscle_skeletal = models.FloatField('Muscle-Skeletal', max_length=10)
    nerve_tibial = models.FloatField('Nerve-Tibial', max_length=10)
    ovary = models.FloatField('Ovary', max_length=10)
    pancreas = models.FloatField('Pancreas', max_length=10)
    pituitary = models.FloatField('Pituitary', max_length=10)
    prostate = models.FloatField('Prostate', max_length=10)
    skin_not_sun_exposed_suprapubic = models.FloatField('Skin-NotSunExposed(Suprapubic)', max_length=10)
    skin_sun_exposed_lower_leg = models.FloatField('Skin-SunExposed(Lowerleg)', max_length=10)
    small_intestine_terminal_ileum = models.FloatField('SmallIntestine-TerminalIleum', max_length=10)
    spleen = models.FloatField('SmallIntestine-TerminalIleum', max_length=10)
    stomach = models.FloatField('Stomach', max_length=10)
    testis = models.FloatField('Testis', max_length=10)
    thyroid = models.FloatField('Thyroid', max_length=10)
    uterus = models.FloatField('Uterus', max_length=10)
    vagina = models.FloatField('Vagina', max_length=10)
    whole_blood = models.FloatField('WholeBlood', max_length=10)

    def __str__(self):
        return self.gene_id


class MutationModel(models.Model):
    class Meta:
        managed = True
        db_table = 'gtexome_mutations'

    geneID_CCID = models.CharField(verbose_name='geneID_CCID', primary_key=True, max_length=40)
    allele_freq = models.DecimalField(verbose_name='allele_freq', max_digits=19, decimal_places=18)
    plddt_snv = models.DecimalField(verbose_name='plddt_snv', max_digits=4, decimal_places=1)
    charge_change = models.CharField(verbose_name='charge_change', max_length=55)
    disulfide_check = models.CharField(verbose_name='disulfide_check', max_length=28)
    proline_check = models.CharField(verbose_name='proline_check', max_length=25)
    buried = models.CharField(verbose_name='buried', max_length=150)
    hydrogen_bond = models.CharField(verbose_name='hydrogen_bond', max_length=60)
    salt_bridge = models.CharField(verbose_name='salt_bridge', max_length=40)
    recommendation = models.CharField(verbose_name='recommendation', max_length=50)
