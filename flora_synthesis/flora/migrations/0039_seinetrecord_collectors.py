# Generated by Django 4.2.5 on 2023-09-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flora", "0038_collector_first_collection_year_and_more")]

    operations = [
        migrations.AddField(
            model_name="seinetrecord",
            name="collectors",
            field=models.ManyToManyField(blank=True, to="flora.collector"),
        )
    ]
