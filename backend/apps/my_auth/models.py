from django.db import models
from django.contrib.auth import get_user_model


class LoginToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

