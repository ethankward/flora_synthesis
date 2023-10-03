# Generated by Django 4.2.5 on 2023-09-16 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flora", "0015_alter_florarecord_observation_type")]

    operations = [
        migrations.AlterField(
            model_name="checklist",
            name="checklist_type",
            field=models.CharField(
                choices=[
                    ("i", "iNaturalist"),
                    ("s", "SEINet"),
                    ("f", "Flora"),
                    ("p", "Personal collection list"),
                ],
                max_length=1,
            ),
        )
    ]
