# Generated by Django 5.0.7 on 2024-07-18 23:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_question_options_alter_result_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_set', to='core.question'),
        ),
    ]
