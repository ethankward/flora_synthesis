# Generated by Django 4.2.3 on 2023-08-10 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0008_checklisttaxon_observation_types_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklisttaxon',
            name='on_checklists',
        ),
    ]
