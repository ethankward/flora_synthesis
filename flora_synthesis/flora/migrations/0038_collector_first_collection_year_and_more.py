# Generated by Django 4.2.5 on 2023-09-24 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0037_alter_collectoralias_collector'),
    ]

    operations = [
        migrations.AddField(
            model_name='collector',
            name='first_collection_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collector',
            name='last_collection_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]