# Generated by Django 4.2.5 on 2023-09-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0039_seinetrecord_collectors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seinetrecord',
            name='collectors',
            field=models.ManyToManyField(blank=True, related_name='collector_seinet_collection_records', to='flora.collector'),
        ),
    ]
