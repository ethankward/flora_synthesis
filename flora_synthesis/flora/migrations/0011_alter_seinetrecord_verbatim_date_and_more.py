# Generated by Django 4.2.5 on 2023-09-11 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0010_alter_checklistrecordnote_added_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seinetrecord',
            name='verbatim_date',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='seinetrecord',
            name='verbatim_elevation',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]