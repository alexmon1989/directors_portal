from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from machina.apps.forum_member.models import ForumProfile
from machina.apps.forum_conversation.models import Post, Topic
from machina.apps.forum.models import Forum
from machina.conf import settings as machina_settings
from machina.apps.forum_member.forms import ForumProfileForm
from pinax.notifications.views import NoticeSettingsView

from .tokens import account_activation_token
from .forms import SignUpForm, ProfileForm


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


class MyProfileInformationView(LoginRequiredMixin, TemplateView):
    """Отображает страницу профиля авторизированного пользователя."""
    template_name = 'my_auth/my_profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = ForumProfile.objects.filter(user=self.request.user).first()
        # Computes the number of topics added by the considered member
        context['topics_count'] = (
            Topic.objects.filter(approved=True, poster=self.request.user).count()
        )

        # Fetches the recent posts added by the considered user
        forums = self.request.forum_permission_handler.get_readable_forums(
            Forum.objects.all(), self.request.user,
        )
        context['recent_posts'] = (
            Post.approved_objects
                .select_related('topic', 'topic__forum')
                .filter(topic__forum__in=forums, poster=self.request.user)
                .order_by('-created')
        )
        context['recent_posts'] = context['recent_posts'][:machina_settings.PROFILE_RECENT_POSTS_NUMBER]

        self.request.user.refresh_from_db()

        return context


class MyProfileSettingsView(LoginRequiredMixin, NoticeSettingsView):
    """Отображает страницу с настройками учётной записи пользователя."""
    template_name = 'my_auth/my_profile/settings/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['action'] = self.request.POST.get('action')

        if context['action'] == 'edit_profile':
            # Редактирование данных профиля
            context['profile_form'] = ProfileForm(data=request.POST, instance=request.user)
            context['forum_profile_form'] = ForumProfileForm(
                data=request.POST,
                files=request.FILES,
                instance=context['profile']
            )
            if context['profile_form'].is_valid() and context['forum_profile_form'].is_valid():
                context['profile_form'].save()
                context['forum_profile_form'].save()
                messages.info(request, 'Настройки успешно сохранены.')
                return redirect('my_profile_settings')

        elif context['action'] == 'edit_security':
            # Редактирование пароля
            context['password_change_form'] = PasswordChangeForm(data=request.POST, user=request.user)
            if context['password_change_form'].is_valid():
                context['password_change_form'].save()
                login(request, request.user)
                messages.info(request, 'Настройки успешно сохранены.')
                return redirect('my_profile_settings')

        elif context['action'] == 'edit_notifications':
            # Редактирование настроек уведомлений
            table = self.settings_table()
            for row in table:
                for cell in row["cells"]:
                    self.process_cell(cell[0])
            messages.info(request, 'Настройки успешно сохранены.')
            return redirect('my_profile_settings')

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = ForumProfile.objects.filter(user=self.request.user).first()
        context.update({
            'action': self.request.GET.get('action', 'edit_profile'),
            'profile': profile,
            'profile_form': ProfileForm(instance=self.request.user),
            'forum_profile_form': ForumProfileForm(instance=profile),
            'password_change_form': PasswordChangeForm(user=self.request.user),
        })
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    """Отображает страницу профиля пользователя."""
    template_name = 'my_auth/profile/index.html'
    model = ForumProfile
    context_object_name = 'profile'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        # Если это профиль текущего пользователя, то производится переадресация его на страницу my_profile
        if self.object.user == self.request.user:
            return redirect('my_profile')
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.model.objects.filter(user=self.kwargs['pk']).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Computes the number of topics added by the considered member
        context['topics_count'] = (
            Topic.objects.filter(approved=True, poster=self.object.user).count()
        )

        # Fetches the recent posts added by the considered user
        forums = self.request.forum_permission_handler.get_readable_forums(
            Forum.objects.all(), self.object.user,
        )
        context['recent_posts'] = (
            Post.approved_objects
                .select_related('topic', 'topic__forum')
                .filter(topic__forum__in=forums, poster=self.object.user)
                .order_by('-created')
        )
        context['recent_posts'] = context['recent_posts'][:machina_settings.PROFILE_RECENT_POSTS_NUMBER]

        return context


class UsersListView(LoginRequiredMixin, ListView):
    """Отображает список пользователей портала."""
    template_name = 'my_auth/my_profile/profiles_list/index.html'
    model = get_user_model()
    queryset = get_user_model().objects.order_by('last_name', 'first_name', 'middle_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ForumProfile.objects.filter(user=self.request.user).first()
        return context
