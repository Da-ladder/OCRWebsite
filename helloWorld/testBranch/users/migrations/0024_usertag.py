# Generated by Django 5.0.6 on 2024-08-29 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_clubdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagName', models.CharField(max_length=255)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.club')),
                ('userList', models.ManyToManyField(blank=True, to='users.users')),
            ],
        ),
    ]
