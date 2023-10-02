from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser

from friend.models import Friend
from friend.serializer import UserFriendSerializer, GetAllUserFriendSerializer


class UserFriend(CreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = UserFriendSerializer

    # authentication_classes =

    def post(self, request, *args, **kwargs):

        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=request.user)
            friend = User.objects.get(username=request.data.get('friend'))
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if Friend.objects.filter(user=user, friend=friend).exists():
            return Response({'error': 'Friendship already exists'}, status=status.HTTP_400_BAD_REQUEST)

        friend_relationship = Friend(user=user, friend=friend)
        friend_relationship.save()

        return Response({'message': 'Friendship created successfully'}, status=status.HTTP_201_CREATED)


class GetAllUserFriend(ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = GetAllUserFriendSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user)
            friend = User.objects.get(username=request.data['friendAccess'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        all_friends = Friend.objects.filter(user=user)
        return Response(self.serializer_class(all_friends, many=True).data, status=status.HTTP_200_OK)
