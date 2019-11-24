from django.shortcuts import render
from apps.news.models import News
from django.utils import timezone


def index(request):
    """Отображает главную страницу."""
    news = News.objects.filter(
        is_on_home=True,
        is_visible=True,
        published_at__gte=timezone.now()
    ).order_by('-published_at')

    return render(
        request,
        'home/index.html',
        {
            'news': news
        }
    )
