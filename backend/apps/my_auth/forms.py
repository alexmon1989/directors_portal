from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm


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
