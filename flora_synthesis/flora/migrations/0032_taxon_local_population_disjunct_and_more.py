# Generated by Django 4.2.5 on 2023-09-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0031_alter_personalcollectionrecord_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='local_population_disjunct',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_eastern_edge_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_northern_edge_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_southern_edge_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_strict_eastern_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_strict_northern_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_strict_southern_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_strict_western_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxon',
            name='local_population_western_edge_range_limit',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]