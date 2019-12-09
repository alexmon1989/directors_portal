from django.urls import path
from .views import SignUpView, SignUpDone, PasswordChangeView, PasswordChangeDone, activate, my_profile, profile_details

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign_up"),
    path('sign-up-done/', SignUpDone.as_view(), name="sign_up_done"),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDone.as_view(), name="password_change_done"),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('me/', my_profile, name='my_profile'),
    path('profile/<int:user_id>', profile_details, name='profile_details'),
]
