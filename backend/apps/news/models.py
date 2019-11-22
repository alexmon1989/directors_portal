from django.db import models
from django.shortcuts import reverse
from backend.abstract_models import TimeStampedModel
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime


class News(TimeStampedModel):
    """Можель новостей."""
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField(unique=True)
    short_text = RichTextField('Короткий текст', blank=True, null=True)
    full_text = RichTextUploadingField('Полный текст', blank=True, null=True)
    image = models.ImageField('Изображение', blank=True, null=True, upload_to='news/%Y/%m/%d/')
    is_visible = models.BooleanField('Отображать', default=True)
    is_on_home = models.BooleanField('Отображать на главной странице', default=True)
    published_at = models.DateTimeField('Опубликовано', default=datetime.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
