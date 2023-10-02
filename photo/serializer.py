from rest_framework import serializers

from photo.models import UserAvatar, Photo, AccessPhoto


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ('image', 'linkPhoto',)


class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessPhoto
        fields = ('friend',)


class UserLoadPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('image',)
