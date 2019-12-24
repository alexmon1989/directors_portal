from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField('Имя', max_length=255)
    middle_name = models.CharField('Отчество', max_length=255, default='')
    last_name = models.CharField('Фамилия', max_length=255)
    organization = models.CharField('Образовательная организация', max_length=255, default='', blank=True)
    address = models.CharField('Страна/регион/город', max_length=255, default='', null=True, blank=True)
    phone = models.CharField('Контактный телефон', max_length=255, default='', null=True, blank=True)
    date_joined = models.DateTimeField('Профиль создан', auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )
    last_activity = models.DateTimeField('Дата последней активности', null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    def get_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def is_online(self):
        """Возвращает True, если последняя активность пользователя была менее чем 15 минут назад."""
        if self.last_activity:
            now = timezone.now()
            then = self.last_activity
            tdelta = now - then
            minutes = tdelta.total_seconds() / 60
            return minutes < 15
        return False

    @property
    def username(self):
        return self.email

    def __str__(self):
        return self.email


class ProxyUser(User):

    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = _('user')
        verbose_name_plural = _('users')
