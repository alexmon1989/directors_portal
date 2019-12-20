from django.contrib import admin
from .models import Question, Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_visible',
        'weight',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_visible',
    )
    search_fields = (
        'title',
    ),
    list_editable = ('weight', 'is_visible')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_visible',
        'weight',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_visible',
    )
    search_fields = (
        'title',
    ),
    list_editable = ('is_visible', 'weight',)
