from django.utils import timezone
from django.contrib.auth import get_user_model


class UpdateLastActivityMiddleware(object):
    """Обновляет при каждом запросе поле last_activity модели User."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = get_user_model().objects.select_for_update().get(pk=request.user.id)
            user.last_activity = timezone.now()
            user.save()
        response = self.get_response(request)
        return response
