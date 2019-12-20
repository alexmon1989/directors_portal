from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch

from .models import Section, Question


class SectionListView(LoginRequiredMixin, ListView):
    """Отображает страницу FAQ."""
    queryset = Section.objects.filter(
        is_visible=True
    ).order_by(
        '-weight'
    ).prefetch_related(
        Prefetch(
            'question_set',
            queryset=Question.objects.filter(is_visible=True).order_by('-weight'))
    )
    model = Section
    template_name = 'faq/index.html'
