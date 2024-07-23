# Generated by Django 5.0.7 on 2024-07-20 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_question_answers_alter_question_correct_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AddField(
            model_name='dragdropitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='drag_drop_images/'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MC', 'Multiple Choice'), ('DD', 'Drag and Drop'), ('SIM', 'Simulation'), ('MAT', 'Matching'), ('FIB', 'Fill in the Blank')], max_length=3),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='DragDropZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('correct_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correct_for_zones', to='core.dragdropitem')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drag_drop_zones', to='core.question')),
            ],
        ),
    ]
