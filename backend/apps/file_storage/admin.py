from django.contrib import admin
from .models import Section, File


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_visible',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_visible',
    )
    search_fields = (
        'title',
    ),
    list_editable = ('is_visible',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'is_confirmed',
        'is_visible',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_confirmed', 'is_visible',
    )
    search_fields = (
        'title',
    ),
    list_editable = ('is_confirmed', 'is_visible',)

