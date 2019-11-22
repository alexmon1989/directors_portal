from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_visible',
        'published_at',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_visible',
    )
    search_fields = (
        'title',
    )
    prepopulated_fields = {"slug": ("title",)}
