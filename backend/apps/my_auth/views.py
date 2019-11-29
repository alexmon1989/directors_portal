from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm


class MyLoginView(LoginView):
    """Класс для управления авторизацией пользователей."""

    def form_valid(self, form):
        """Авторизирует пользователя и возвращает код 200, если логин и пароль верны."""
        login(self.request, form.get_user())

        # Если пользователь не нажал "Запомнить меня", то сессия заканчивается при закрытии браузера.
        if not int(self.request.POST['rememberme']):
            self.request.session.set_expiry(0)
        return HttpResponse(status=200)

    def form_invalid(self, form):
        """Возвращает код 400, если введены неверные логин, пароль."""
        return HttpResponse(status=400)


class SignUpView(FormView):
    """Регистрация пользователя."""

    template_name = 'registration/sign_up.html'
    form_class = SignUpForm
    success_url = '/accounts/sign-up-done/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SignUpDone(TemplateView):
    """Страница оповещения успешной регистрации."""
    template_name = 'registration/sign_up_done.html'


class PasswordChangeView(LoginRequiredMixin, FormView):
    """Смена пароля пользователем"""

    template_name = 'registration/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = '/accounts/password-change-done/'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)


class PasswordChangeDone(LoginRequiredMixin, TemplateView):
    """Страница оповещения успешной смены пароля."""
    template_name = 'registration/password_change_done.html'
