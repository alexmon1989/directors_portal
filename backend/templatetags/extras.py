from django import template
from apps.news.models import News
from datetime import datetime

register = template.Library()


@register.inclusion_tag('templatetags/last_news_footer.html')
def last_news_footer():
    news = News.objects.filter(
        is_visible=True,
        published_at__lte=datetime.now()
    ).order_by('-published_at')

    return {'news': news}
