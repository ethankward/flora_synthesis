# Generated by Django 4.2.5 on 2023-09-16 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0016_alter_checklist_checklist_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='collector_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
