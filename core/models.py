# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import sys

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
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.test.title} - Question {self.order}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    def resize_image(self, image):
        img = Image.open(image)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img = img.resize(output_size, Image.LANCZOS)
            output = io.BytesIO()
            
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
                img.save(output, format='PNG', quality=85)
                file_extension = 'png'
                mime = 'image/png'
            else:
                img = img.convert('RGB')
                img.save(output, format='JPEG', quality=85)
                file_extension = 'jpg'
                mime = 'image/jpeg'
            
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField', 
                                        f"{image.name.split('.')[0]}.{file_extension}", 
                                        mime, 
                                        sys.getsizeof(output), None)
        return image

    class Meta:
        ordering = ['order']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.question}"

class DragDropItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='drag_drop_items')
    text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='drag_drop_images/', null=True, blank=True)
    correct_position = models.IntegerField()

    def __str__(self):
        return f"Drag-drop item for {self.question}: {self.text}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    def resize_image(self, image):
        img = Image.open(image)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img = img.resize(output_size, Image.LANCZOS)
            output = io.BytesIO()
            
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
                img.save(output, format='PNG', quality=85)
                file_extension = 'png'
                mime = 'image/png'
            else:
                img = img.convert('RGB')
                img.save(output, format='JPEG', quality=85)
                file_extension = 'jpg'
                mime = 'image/jpeg'
            
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField', 
                                        f"{image.name.split('.')[0]}.{file_extension}", 
                                        mime, 
                                        sys.getsizeof(output), None)
        return image

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