# Generated by Django 4.2.5 on 2023-09-22 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0033_alter_taxon_life_cycle'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='has_collections',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
