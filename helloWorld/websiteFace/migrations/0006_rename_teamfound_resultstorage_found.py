# Generated by Django 5.0 on 2024-06-24 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websiteFace', '0005_resultstorage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultstorage',
            old_name='teamFound',
            new_name='found',
        ),
    ]
