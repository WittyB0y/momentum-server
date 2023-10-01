from django.contrib import admin
from django.urls import path, include

from user.views import RegistrUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/register', RegistrUserView.as_view(), name='registr')
]
