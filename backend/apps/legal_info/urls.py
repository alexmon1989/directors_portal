from django.urls import path
from .views import LinkListView

app_name = 'legal_info'
urlpatterns = [
    path('', LinkListView.as_view(), name="index"),
]
