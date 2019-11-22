from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактный класс модели, содержащий описания полей created, modified."""
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        abstract = True
