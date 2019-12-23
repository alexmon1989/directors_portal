from django.db import models
from backend.abstract_models import TimeStampedModel


class Link(TimeStampedModel):
    """Модель ссылки на ресурс."""
    title = models.CharField('Название', max_length=255)
    link = models.URLField('Ссылка')
    weight = models.PositiveIntegerField(
        'Вес',
        default=1000,
        help_text='Чем выше вес, тем выше расположен элемент на странице.'
    )
    is_visible = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
