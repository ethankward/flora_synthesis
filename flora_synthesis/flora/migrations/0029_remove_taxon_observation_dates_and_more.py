# Generated by Django 4.2.5 on 2023-09-19 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("flora", "0028_taxon_first_observation_date_and_more")]

    operations = [
        migrations.RemoveField(model_name="taxon", name="observation_dates"),
        migrations.DeleteModel(name="ObservationDate"),
    ]
