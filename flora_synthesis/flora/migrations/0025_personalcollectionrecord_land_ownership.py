# Generated by Django 4.2.5 on 2023-09-18 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flora", "0024_personalcollectionrecord_description")]

    operations = [
        migrations.AddField(
            model_name="personalcollectionrecord",
            name="land_ownership",
            field=models.TextField(blank=True, null=True),
        )
    ]
