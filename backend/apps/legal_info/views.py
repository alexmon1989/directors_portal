from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Link


class LinkListView(LoginRequiredMixin, ListView):
    """Отображает страницу Правовая информация."""
    queryset = Link.objects.filter(
        is_visible=True
    ).order_by(
        '-weight'
    )
    model = Link
    template_name = 'legal_info/index.html'
