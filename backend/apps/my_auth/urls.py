from django.urls import path
from .views import (SignUpView, SignUpDone, PasswordChangeView, PasswordChangeDone, activate, MyProfileInformationView,
                    ProfileView, MyProfileSettingsView, UsersListView)

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign_up"),
    path('sign-up-done/', SignUpDone.as_view(), name="sign_up_done"),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDone.as_view(), name="password_change_done"),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('me/', MyProfileInformationView.as_view(), name='my_profile'),
    path('me/settings/', MyProfileSettingsView.as_view(), name='my_profile_settings'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_details'),
    path('profiles-list/', UsersListView.as_view(), name='profiles_list'),
]
