# Generated by Django 5.0.7 on 2024-07-19 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_question_answers_question_correct_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='answers',
            field=models.TextField(help_text="JSON containing user's answers"),
        ),
    ]
