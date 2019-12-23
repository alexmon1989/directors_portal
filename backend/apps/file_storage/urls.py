from django.urls import path
from .views import (SectionListView, FileListView, FileDetailView, FileDeleteView, MyFileStorage, FileCreateView,
                    FileUpdateView)

app_name = 'file_storage'
urlpatterns = [
    path('', SectionListView.as_view(), name="section-list"),
    path('section/<int:pk>/', FileListView.as_view(), name="file-list"),
    path('file/detail/<int:pk>/', FileDetailView.as_view(), name="file-detail"),
    path('file/delete/<int:pk>/', FileDeleteView.as_view(), name="file-delete"),
    path('me/', MyFileStorage.as_view(), name="my-file-storage"),
    path('create-file/', FileCreateView.as_view(), name="create-file"),
    path('update-file/<int:pk>/', FileUpdateView.as_view(), name="update-file"),
]
