# Generated by Django 5.0.6 on 2024-07-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_club_homeurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='extraData',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='picURL',
            field=models.URLField(blank=True, null=True),
        ),
    ]
