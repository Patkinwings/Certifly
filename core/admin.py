# core/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect, render
from .models import User, Test, Question, Answer, DragDropItem, DragDropZone, MatchingItem, Simulation, Result, FillInTheBlank

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('username', 'email')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class DragDropItemInline(admin.TabularInline):
    model = DragDropItem
    extra = 4

class DragDropZoneInline(admin.TabularInline):
    model = DragDropZone
    extra = 4

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "correct_item" and hasattr(self, 'parent_obj'):
            kwargs["queryset"] = DragDropItem.objects.filter(question=self.parent_obj)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FillInTheBlankInline(admin.TabularInline):
    model = FillInTheBlank
    extra = 1

class MatchingItemInline(admin.TabularInline):
    model = MatchingItem
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'question_type', 'order', 'image_preview')
    list_filter = ('test', 'question_type')
    search_fields = ('text', 'test__title')
    raw_id_fields = ('test',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('test')

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.question_type == 'MC':
                return [AnswerInline]
            elif obj.question_type == 'DD':
                return [DragDropItemInline, DragDropZoneInline]
            elif obj.question_type == 'MAT':
                return [MatchingItemInline]
            elif obj.question_type == 'FIB':
                return [FillInTheBlankInline]
        return []

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image Preview'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit', 'created_at')
    search_fields = ('title',)
    list_per_page = 20

@admin.register(DragDropItem)
class DragDropItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'correct_position', 'image_preview')
    list_filter = ('question',)
    search_fields = ('text', 'question__text')
    raw_id_fields = ('question',)
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image Preview'

@admin.register(DragDropZone)
class DragDropZoneAdmin(admin.ModelAdmin):
    list_display = ('question', 'label', 'correct_item')
    list_filter = ('question',)
    search_fields = ('label', 'question__text')
    raw_id_fields = ('question', 'correct_item')
    list_per_page = 20

@admin.register(MatchingItem)
class MatchingItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'left_side', 'right_side')
    list_filter = ('question',)
    search_fields = ('left_side', 'right_side', 'question__text')
    raw_id_fields = ('question',)
    list_per_page = 20

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('question', 'initial_state')
    list_filter = ('question',)
    search_fields = ('initial_state', 'expected_commands', 'question__text')
    raw_id_fields = ('question',)
    list_per_page = 20

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'created_at')
    list_filter = ('test', 'created_at')
    search_fields = ('user__username', 'test__title')
    raw_id_fields = ('user', 'test')
    list_per_page = 20

@admin.register(FillInTheBlank)
class FillInTheBlankAdmin(admin.ModelAdmin):
    list_display = ('question', 'blank_index', 'correct_answer')
    list_filter = ('question',)
    search_fields = ('correct_answer', 'question__text')
    raw_id_fields = ('question',)
    list_per_page = 20