# Generated by Django 5.0.6 on 2024-08-29 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_club_applicationinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=2000, null=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.club')),
            ],
        ),
    ]
