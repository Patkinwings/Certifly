# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from cloudinary.models import CloudinaryField


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename

class User(AbstractUser):
    payment_status = models.BooleanField(default=False)

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('MC', 'Multiple Choice'),
        ('DD', 'Drag and Drop'),
        ('SIM', 'Simulation'),
        ('MAT', 'Matching'),
        ('FIB', 'Fill in the Blank'),
    )
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', db_index=True)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES, db_index=True)
    text = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f"{self.test.title} - Question {self.order}"

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['test', 'question_type', 'order']),
        ]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.question}"

class DragDropItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='drag_drop_items')
    text = models.CharField(max_length=200)
    image = CloudinaryField('image', null=True, blank=True)
    correct_position = models.IntegerField()

    def __str__(self):
        return f"Drag-drop item for {self.question}: {self.text}"

class DragDropZone(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='drag_drop_zones')
    label = models.CharField(max_length=200)
    correct_item = models.ForeignKey(DragDropItem, on_delete=models.CASCADE, related_name='correct_for_zones')

    def __str__(self):
        return f"Drop zone for {self.question}: {self.label}"

class MatchingItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='matching_items')
    left_side = models.CharField(max_length=200)
    right_side = models.CharField(max_length=200)

    def __str__(self):
        return f"Matching item for {self.question}: {self.left_side} - {self.right_side}"

class Simulation(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='simulations')
    initial_state = models.TextField()
    expected_commands = models.TextField()

    def __str__(self):
        return f"Simulation for {self.question}"

class FillInTheBlank(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='fill_in_the_blanks')
    blank_index = models.IntegerField()
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"Fill in the blank for {self.question}: {self.correct_answer}"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    answers = models.TextField(help_text="JSON containing user's answers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}"

    class Meta:
        ordering = ['-created_at']