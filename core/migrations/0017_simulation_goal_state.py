# Generated by Django 4.2.3 on 2024-08-05 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_result_category_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='goal_state',
            field=models.TextField(blank=True, null=True),
        ),
    ]
