from django.urls import path

from user.views import RegisterUserView, CheckIsAvailableUsername

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('check/', CheckIsAvailableUsername.as_view(), name='check_is_available_username'),
]
