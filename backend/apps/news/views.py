from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import News


class NewsListView(ListView):
    """Отображает страницу со списком новостей."""
    model = News
    paginate_by = 6
    template_name = 'news/list/index.html'

    def get_queryset(self):
        return News.objects.filter(is_visible=True, published_at__lte=timezone.now()).order_by('-published_at')


class NewsDetailView(DetailView):
    """Отображает страницу со списком новостей."""
    template_name = 'news/detail/index.html'

    def get_queryset(self):
        return News.objects.filter(is_visible=True, published_at__lte=timezone.now()).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_news'] = self.get_queryset().exclude(slug=self.kwargs['slug'])[:15]
        return context
