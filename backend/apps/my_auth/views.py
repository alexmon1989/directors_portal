from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail
from machina.apps.forum_member.models import ForumProfile
from .tokens import account_activation_token
from .forms import SignUpForm


class MyLoginView(LoginView):
    """Класс для управления авторизацией пользователей."""

    def form_valid(self, form):
        """Авторизирует пользователя и возвращает код 200, если логин и пароль верны."""
        # Если пользователь не нажал "Запомнить меня", то сессия заканчивается при закрытии браузера.
        if not int(self.request.POST.get('rememberme', 0)):
            self.request.session.set_expiry(0)

        return super().form_valid(form)


class SignUpView(FormView):
    """Регистрация пользователя."""

    template_name = 'registration/sign_up.html'
    form_class = SignUpForm
    success_url = '/accounts/sign-up-done/'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        group = Group.objects.get(name='General users')
        group.user_set.add(user)

        current_site = get_current_site(self.request)
        message = render_to_string('registration/account_activation_email.txt', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        html_message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        subject = 'Активируйте вашу учётную запись'
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[user.email],
            from_email=None
        )

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


def activate(request, uidb64, token):
    """Активирует учётную запись."""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home:index')
    else:
        return HttpResponse('invalid token')


@login_required
def my_profile(request):
    profile = ForumProfile.objects.filter(user=request.user).first()
    return render(request, 'my_auth/my_profile/index.html', {'profile': profile})
