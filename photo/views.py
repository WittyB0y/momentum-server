import os
import uuid

from django.contrib.auth.models import User, AnonymousUser
from django.core.files.base import ContentFile
from django.http import FileResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from photo.models import Photo, AccessPhoto
from photo.protectPhoto import encrypting, decrypting
from photo.serializer import UserLoadPhotoSerializer


def rename_file(name, image):
    file_extension = os.path.splitext(image.name)[-1].lower()
    image.name = f'{name}.{file_extension}'
    return image.name, file_extension


class LoadPhoto(CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = UserLoadPhotoSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)

        try:
            user = User.objects.get(username=request.user)
            friend = User.objects.get(id=kwargs.get('userid'))
            if user == friend:
                return Response(
                    {'error': "You can't send data to yourself."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if file_serializer.is_valid():
            name_uuid = uuid.uuid4()
            new_name = rename_file(name_uuid, request.data['image'])
            encrypted_data = encrypting(request.data['image'])

            temp_file = ContentFile(encrypted_data.read())
            temp_file.name = f'{name_uuid}.crp'

            file_serializer.save(
                owner=user,
                dataType=new_name[1],
                filename=name_uuid,
                image=temp_file,
            )
            check_exists = AccessPhoto.objects.filter(photo__owner_id=user, friend=friend).exists()
            if check_exists:
                AccessPhoto.objects.filter(photo__owner_id=user, friend=friend).delete()
            AccessPhoto(
                photo=file_serializer.instance,
                friend=friend,
            ).save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNewPhoto(ListAPIView):
    queryset = AccessPhoto.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user

        if isinstance(user, AnonymousUser):
            return Response({'error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            last_photo = self.queryset.filter(friend=user).latest('id')
        except AccessPhoto.DoesNotExist:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        data = Photo.objects.get(id=last_photo.photo_id).filename
        return Response({'photo': data})


class GetDecryptingImage(ListAPIView):
    queryset = AccessPhoto.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user

        if isinstance(user, AnonymousUser):
            return Response({'error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        file = Photo.objects.get(filename=request.data['name'])
        access = self.queryset.filter(photo_id=file.id, friend=user)

        if not access.exists():
            return Response({'error': 'not access'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(file=f'media/{file.image}', mode='rb') as f:
                image = decrypting(f)
        except FileNotFoundError:
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(image, content_type='image/jpeg')
