# Generated by Django 5.0 on 2024-06-28 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_club_active_club_advisororadvisors_club_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='discription',
            field=models.TextField(blank=True),
        ),
    ]
