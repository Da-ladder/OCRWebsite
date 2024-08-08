# Generated by Django 5.0.6 on 2024-08-08 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_replies_replylink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replies',
            name='replyLink',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='OriginalReply', to='users.replies'),
        ),
    ]
