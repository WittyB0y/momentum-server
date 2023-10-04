import re

from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register user.
    """
    email: str = serializers.EmailField(max_length=500)
    password: str = serializers.CharField(max_length=128)

    class Meta:
        model: User = User
        fields: tuple['str'] = ('username', 'first_name', 'email', 'password',)

    def validate(self, attrs):
        if not re.match(r'^[a-zA-Z0-9/./+/-/_]{3,150}$', attrs['username']):
            raise serializers.ValidationError(
                'Incorrect username.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not re.match(r'^[a-zA-Zа-яА-Я ]{1,150}$', attrs['first_name']):
            raise serializers.ValidationError(
                'Incorrect first_name.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,128}$',
                attrs['password'],
        ):
            raise serializers.ValidationError(
                'Incorrect password.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        attrs['username'] = attrs['username'].capitalize()
        attrs['first_name'] = attrs['first_name'].capitalize()
        attrs['email'] = attrs['email'].lower()
        return attrs

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields: tuple['str'] = ('id', 'username', 'last_name', 'first_name',)
