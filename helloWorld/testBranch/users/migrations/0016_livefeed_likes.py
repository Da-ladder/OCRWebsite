# Generated by Django 5.0.6 on 2024-08-07 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_rename_picture_url_club_homeurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='livefeed',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
