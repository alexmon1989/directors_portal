from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import LoginToken
import hashlib
from django.utils import timezone



class SignUpForm(UserCreationForm):
    """Класс формы регистрации. Расширяет базовый класс формы UserCreationForm."""
    first_name = forms.CharField(max_length=255, label='Имя')
    last_name = forms.CharField(max_length=255, label='Фамилия')
    middle_name = forms.CharField(max_length=255, label='Отчество')
    email = forms.EmailField(max_length=255, label='E-Mail')
    organization = forms.CharField(max_length=255, label='Образовательная организация')
    phone = forms.CharField(max_length=255, label='Контактный телефон')
    rules_agree = forms.BooleanField()

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'organization',
            'phone',
            'password1',
            'password2',
        )


class ProfileForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'last_name',
            'first_name',
            'middle_name',
            'organization',
            'address',
            'phone',
        )


class LoginConfirmationForm(forms.Form):
    value = forms.CharField(
        max_length=255,
        label='Код',
        help_text='Для подтверждения входа на сайт на ваш E-Mail был направлен код. '
                  'Пожалуйста, введите его в поле ниже и нажмите кнопку "Подтвердить".'
    )

    def __init__(self, user_id, *args, **kwargs):
        self.user = get_user_model().objects.get(pk=user_id)
        super().__init__(*args, **kwargs)

    def clean_value(self):
        value = self.cleaned_data['value']
        login_token = LoginToken.objects.order_by('-created_at').filter(
            user=self.user,
            created_at__gte=(timezone.now() - timezone.timedelta(minutes=15))
        ).first()
        if not login_token or login_token.value != hashlib.sha256(value.encode()).hexdigest():
            raise forms.ValidationError("Вы ввели неверный код!")
        return value
