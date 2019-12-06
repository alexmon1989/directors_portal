from django.utils import timezone

from apps.core_app.models import User


class UpdateLastActivityMiddleware(object):
    def process_request(self, request):
        assert hasattr(request,
                       'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            User.objects.filter(user__id=request.user.id).update(last_activity=timezone.now())
