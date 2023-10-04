from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from friend.views import UserFriend, GetAllUserFriend
from momentumServer import settings
from photo.views import LoadPhoto, GetNewPhoto, GetDecryptingImage
from user.views import RegistrUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/register', RegistrUserView.as_view(), name='register'),
    path('add_friend/', UserFriend.as_view(), name='add_friend'),
    path('api/v1/friends/', GetAllUserFriend.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/load_photo/<int:userid>/', LoadPhoto.as_view()),
    path('api/v1/get_new_photo/', GetNewPhoto.as_view()),
    path('api/v1/get/', GetDecryptingImage.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
