from django.urls import path

from photo.views import UploadPhoto, GetNewPhoto, GetDecryptingImage

urlpatterns = [
    path('upload/<int:userid>/', UploadPhoto.as_view(), name='upload_photo'),
    path('get_new/', GetNewPhoto.as_view(), name='get_new_photo'),
    path('get_decrypting/', GetDecryptingImage.as_view(), name='get_decrypting_photo'),
]
