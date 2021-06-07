# Generated by Django 3.1.7 on 2021-04-29 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DrugNamePrecursorMap',
            fields=[
                ('drug_name', models.CharField(max_length=100, verbose_name='drug_name')),
                ('precursor_UUID', models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='precursor_UUID')),
                ('precursor_DrugID', models.CharField(max_length=12, verbose_name='precursor_DrugID')),
            ],
            options={
                'db_table': 'drug_name_precursor_map',
                'managed': True,
            },
        ),
    ]