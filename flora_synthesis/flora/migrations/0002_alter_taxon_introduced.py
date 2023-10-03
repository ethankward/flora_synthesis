# Generated by Django 4.2.3 on 2023-09-04 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flora", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="taxon",
            name="introduced",
            field=models.CharField(
                blank=True,
                choices=[
                    ("i", "Introduced"),
                    ("n", "Native"),
                    ("p", "Possibly introduced"),
                ],
                max_length=1,
                null=True,
            ),
        )
    ]
