# Generated by Django 4.2.5 on 2023-09-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0040_alter_seinetrecord_collectors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collector',
            name='external_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]