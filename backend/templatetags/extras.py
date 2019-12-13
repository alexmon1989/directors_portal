from django import template
from apps.news.models import News
from django.utils import timezone
from django.contrib.auth import get_user_model
import urllib.parse

register = template.Library()


@register.inclusion_tag('templatetags/last_news_footer.html')
def last_news_footer():
    news = News.objects.filter(
        is_visible=True,
        published_at__lte=timezone.now()
    ).order_by('-published_at')

    return {'news': news}


@register.simple_tag
def replace_and_urlencode(get_params, field, value):
    get_params[field] = value
    return urllib.parse.urlencode(get_params, doseq=True)


@register.inclusion_tag('templatetags/pagination.html')
def pagination(page_obj, get_params):
    return {
        'page_obj': page_obj,
        'get_params': get_params.dict(),
    }


@register.simple_tag
def get_name_by_email(email):
    print(get_user_model().objects.filter(email=email).first().get_name())
    return get_user_model().objects.filter(email=email).first().get_name()
