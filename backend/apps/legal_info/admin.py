from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'link',
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
    list_editable = (
        'weight',
        'is_visible'
    )
