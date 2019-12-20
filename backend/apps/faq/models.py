from django.db import models
from backend.abstract_models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField


class Section(TimeStampedModel):
    """Модель раздела."""
    title = models.CharField('Название раздела', max_length=255)
    weight = models.PositiveIntegerField(
        'Вес',
        default=1000,
        help_text='Чем выше вес, тем выше расположен элемент на странице.'
    )
    is_visible = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Question(TimeStampedModel):
    """Модель вопроса."""
    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел')
    title = models.CharField('Название вопроса', max_length=255)
    answer = RichTextUploadingField('Ответ', blank=True)
    weight = models.PositiveIntegerField(
        'Вес',
        default=1000,
        help_text='Чем выше вес, тем выше расположен элемент на странице.'
    )
    is_visible = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
