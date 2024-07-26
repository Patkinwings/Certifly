# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Question, Test, Answer, DragDropItem, DragDropZone, FillInTheBlank

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'text', 'order']

class QuestionImageForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, max_num=4, can_delete=False)

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'time_limit']

class DragDropItemForm(forms.ModelForm):
    class Meta:
        model = DragDropItem
        fields = ['text', 'image', 'correct_position']

DragDropItemFormSet = forms.inlineformset_factory(Question, DragDropItem, form=DragDropItemForm, extra=4, max_num=10, can_delete=True)

class DragDropZoneForm(forms.ModelForm):
    class Meta:
        model = DragDropZone
        fields = ['label', 'correct_item']

DragDropZoneFormSet = forms.inlineformset_factory(Question, DragDropZone, form=DragDropZoneForm, extra=4, max_num=10, can_delete=True)

class FillInTheBlankForm(forms.ModelForm):
    class Meta:
        model = FillInTheBlank
        fields = ['blank_index', 'correct_answer']

FillInTheBlankFormSet = forms.inlineformset_factory(Question, FillInTheBlank, form=FillInTheBlankForm, extra=1, max_num=10, can_delete=True)