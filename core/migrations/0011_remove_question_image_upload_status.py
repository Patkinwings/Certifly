# Generated by Django 4.2.3 on 2024-07-27 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_merge_20240726_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image_upload_status',
        ),
    ]
