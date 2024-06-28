# Generated by Django 5.0 on 2024-06-24 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websiteFace', '0004_remove_videostorage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamFound', models.CharField(max_length=10)),
                ('vid_name', models.CharField(max_length=100)),
                ('vid_links', models.TextField(blank=True, null=True)),
            ],
        ),
    ]