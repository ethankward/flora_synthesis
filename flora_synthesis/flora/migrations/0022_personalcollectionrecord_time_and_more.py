# Generated by Django 4.2.5 on 2023-09-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0021_alter_personalcollectionrecord_collection_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalcollectionrecord',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalcollectionrecord',
            name='date',
            field=models.DateField(),
        ),
    ]