from django.urls import path

from user.views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
]
