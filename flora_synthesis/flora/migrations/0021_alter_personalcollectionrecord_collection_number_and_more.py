# Generated by Django 4.2.5 on 2023-09-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0020_personalcollectionrecord_collection_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalcollectionrecord',
            name='collection_number',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personalcollectionrecord',
            name='date',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
