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

class Category(models.Model):
    CORE_CHOICES = [
        ('CORE1', 'Core 1'),
        ('CORE2', 'Core 2'),
    ]
    DOMAIN_CHOICES = [
        ('MD', 'Mobile Devices'),
        ('NW', 'Networking'),
        ('HW', 'Hardware'),
        ('VC', 'Virtualization and Cloud Computing'),
        ('HNT', 'Hardware and Network Troubleshooting'),
        ('OS', 'Operating Systems'),
        ('SEC', 'Security'),
        ('ST', 'Software Troubleshooting'),
        ('OP', 'Operational Procedures'),
    ]

    core = models.CharField(max_length=5, choices=CORE_CHOICES)
    domain = models.CharField(max_length=3, choices=DOMAIN_CHOICES)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.get_core_display()} - {self.get_domain_display()}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.get_core_display()} - {self.get_domain_display()}"
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('core', 'domain')
        verbose_name_plural = "Categories"

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES, db_index=True)
    text = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    explanation = models.TextField(help_text="Explanation of the correct answer", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

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
    correct_position = models.PositiveIntegerField()

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
    expected_commands = models.TextField()

    def __str__(self):
        return f"Simulation for {self.question}"

class FillInTheBlank(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='fill_in_the_blanks')
    blank_index = models.PositiveIntegerField()
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"Fill in the blank for {self.question}: {self.correct_answer}"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    answers = models.JSONField(help_text="JSON containing user's answers")
    category_scores = models.JSONField(default=dict, help_text="JSON containing category scores")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}"

    class Meta:
        ordering = ['-created_at']

class QuestionResult(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='question_results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.JSONField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Question result for {self.result} - Question {self.question.order}"

    class Meta:
        ordering = ['question__order']