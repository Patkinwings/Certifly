from django.contrib import admin
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "correct_item" and request.resolver_match.kwargs.get('object_id'):
            kwargs["queryset"] = DragDropItem.objects.filter(
                question_id=request.resolver_match.kwargs['object_id']
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FillInTheBlankInline(admin.TabularInline):
    model = FillInTheBlank
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'question_type', 'order', 'image')
    list_filter = ('test', 'question_type')
    search_fields = ('text', 'test__title')

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.question_type == 'MC':
                return [AnswerInline]
            elif obj.question_type == 'DD':
                return [DragDropItemInline, DragDropZoneInline]
            elif obj.question_type == 'MAT':
                return [MatchingItem]
            elif obj.question_type == 'FIB':
                return [FillInTheBlankInline]
        return []

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit', 'created_at')
    search_fields = ('title',)

@admin.register(DragDropItem)
class DragDropItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'correct_position')
    list_filter = ('question',)
    search_fields = ('text', 'question__text')

@admin.register(DragDropZone)
class DragDropZoneAdmin(admin.ModelAdmin):
    list_display = ('question', 'label', 'correct_item')
    list_filter = ('question',)
    search_fields = ('label', 'question__text')

@admin.register(MatchingItem)
class MatchingItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'left_side', 'right_side')
    list_filter = ('question',)
    search_fields = ('left_side', 'right_side', 'question__text')

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('question', 'initial_state')
    list_filter = ('question',)
    search_fields = ('initial_state', 'expected_commands', 'question__text')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'created_at')
    list_filter = ('test', 'created_at')
    search_fields = ('user__username', 'test__title')

@admin.register(FillInTheBlank)
class FillInTheBlankAdmin(admin.ModelAdmin):
    list_display = ('question', 'blank_index', 'correct_answer')
    list_filter = ('question',)
    search_fields = ('correct_answer', 'question__text')