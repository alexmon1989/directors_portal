from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import reverse

from .models import Section, File


class SectionListView(LoginRequiredMixin, ListView):
    """Отображает страницу списка разделов."""
    queryset = Section.objects.filter(
        is_visible=True
    ).order_by(
        'title'
    )
    model = Section
    template_name = 'file_storage/section/list/index.html'


class FileListView(LoginRequiredMixin, ListView):
    """Отображает страницу списка файлов."""
    queryset = File.objects.filter(
        is_visible=True,
        is_confirmed=True
    ).order_by(
        '-created_at'
    )
    model = File
    template_name = 'file_storage/file/list/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(pk=self.kwargs['pk'])
        return context


class FileDetailView(LoginRequiredMixin, DetailView):
    """Отображает страницу детальной информации по файлу."""
    model = File
    template_name = 'file_storage/file/detail/index.html'

    def get_queryset(self):
        q = File.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return q
        else:
            return q.filter(
                user=self.request.user
            )


class FileDeleteView(LoginRequiredMixin, DeleteView):
    """Отображает страницу подтверждения удаления файла."""
    model = File
    template_name = 'file_storage/file/delete/index.html'
    success_message = "Файл был успешно удалён."

    def get_queryset(self):
        q = File.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return q
        else:
            return q.filter(
                user=self.request.user
            )

    def get_success_url(self):
        return reverse('file_storage:file-list', args=[self.object.section.pk])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class MyFileStorage(LoginRequiredMixin, ListView):
    """Отображает страницу списка файлов пользователя."""
    model = File
    template_name = 'file_storage/my_file_storage/index.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        queryset = File.objects.filter(
            is_visible=True,
            user=self.request.user
        ).order_by(
            '-created_at'
        )
        return queryset


class FileCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Отображает страницу добавления файла."""
    model = File
    template_name = 'file_storage/create/index.html'
    fields = [
        'title',
        'section',
        'description',
        'file',
    ]
    success_message = 'Файл успешно сохранён. Он появится на сайте после одобрения модератором.'

    def get_success_url(self):
        return reverse('file_storage:section-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class FileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Отображает страницу обновления файла."""
    model = File
    template_name = 'file_storage/update/index.html'
    fields = [
        'title',
        'section',
        'description',
        'file',
    ]
    success_message = 'Файл успешно сохранён.'

    def get_queryset(self):
        q = File.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return q
        else:
            return q.filter(
                user=self.request.user
            )
