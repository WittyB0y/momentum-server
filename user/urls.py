from django.urls import path

from user.views import RegisterUserView

urlpatterns = [
    path('regiser/', RegisterUserView.as_view(), name='register'),
]
