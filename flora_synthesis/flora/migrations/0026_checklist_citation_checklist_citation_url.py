# Generated by Django 4.2.5 on 2023-09-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flora", "0025_personalcollectionrecord_land_ownership")]

    operations = [
        migrations.AddField(
            model_name="checklist",
            name="citation",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="checklist",
            name="citation_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
