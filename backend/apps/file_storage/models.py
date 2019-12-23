from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from backend.abstract_models import TimeStampedModel


class Section(TimeStampedModel):
    """Модель раздела."""
    title = models.CharField('Название раздела', max_length=255)
    is_visible = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.title

    def get_files_count(self):
        return self.file_set.filter(is_visible=True, is_confirmed=True).count()

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class File(TimeStampedModel):
    """Модель файла."""
    title = models.CharField('Наименование файла', max_length=255)
    description = RichTextField('Описание', null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел')
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    file = models.FileField('Файл', upload_to='file_storage/%Y/%m/%d/')
    is_confirmed = models.BooleanField('Одобрен', default=False)
    is_visible = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('file_storage:file-detail', args=[self.pk])

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
