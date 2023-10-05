from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt import authentication

from friend.models import Friend, RequestToFriend
from friend.serializer import (
    GetAllUserFriendSerializer,
    RequestToFriendSerializer,
    UserFriendSerializer,
)


class RequestToAddFriend(CreateAPIView, ListAPIView, DestroyAPIView):
    """
    create friend request;
    get all incoming friend requests;
    delete incoming friend request.
    """
    queryset = User.objects.all()
    serializer_class = RequestToFriendSerializer
    authentication_classes = (authentication.JWTAuthentication,)

    def filter_queryset(self, queryset):
        match queryset:
            case ('USER'):
                queryset = User.objects.all()
            case ('FRIEND_REQUEST'):
                queryset = RequestToFriend.objects.all()
            case _:
                ...
        return queryset

    def post(self, request, *args, **kwargs):
        """
        create friend request
        """

        if isinstance(request.user, AnonymousUser):
            return Response({'Error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        validated = self.serializer_class().validate_friend(request.data.copy())
        if 'friend' not in validated:
            return Response(
                {
                    'Error': 'friend is required field',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = self.filter_queryset('USER').get(username=request.user)
            friend = self.filter_queryset('USER').get(username=validated.get('friend'))

            if user == friend:
                return Response(
                    {
                        'Error': 'you can not add yourself to friend',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except User.DoesNotExist:
            return Response({'Error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        request_to_db = self.filter_queryset('FRIEND_REQUEST').filter(
            inviter=user.id,
            receiver=friend.id,
        )

        if request_to_db.filter(status=False).exists():
            return Response({'Warning': 'request already sent'}, status=status.HTTP_202_ACCEPTED)
        elif request_to_db.filter(status=True).exists():
            return Response(
                {'Error': 'your request accepted already',
                 },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            request_to_friend = self.filter_queryset('FRIEND_REQUEST').create(
                inviter=user,
                receiver=friend,
            )
            request_to_friend.save()
            return Response({'Success': 'request sent'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """
        get all incoming friend requests
        """
        if isinstance(request.user, AnonymousUser):
            return Response({'Error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = self.filter_queryset('USER').get(username=request.user)
        except User.DoesNotExist:
            return Response({'Error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        all_requests = self.filter_queryset('FRIEND_REQUEST').filter(receiver=user.id, status=False)

        validated = self.serializer_class(all_requests, many=True).data
        response = {
            'count': all_requests.count(),
            'requests': validated,
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        delete friend request
        """
        if isinstance(request.user, AnonymousUser):
            return Response({'Error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        validated = self.serializer_class().validate_friend(request.data.copy())
        if 'friend' not in validated:
            return Response(
                {
                    'Error': 'friend is required field',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            friend = self.filter_queryset('USER').get(username=validated.get('friend'))
        except User.DoesNotExist:
            return Response({'Error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        data_request = self.filter_queryset('FRIEND_REQUEST').filter(
            receiver=request.user,
            inviter=friend.id,
            status=False,
        )

        if not data_request.exists():
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        data_request.delete()
        return Response({'Success': 'request is deleted'}, status=status.HTTP_200_OK)


class GetAllUserFriend(ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = GetAllUserFriendSerializer

    def get(self, request, *args, **kwargs):
        """
        get all friends
        """
        try:
            user = User.objects.get(username=request.user)
            User.objects.get(username=request.data['friendAccess'])
        except User.DoesNotExist:
            return Response({'Error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        all_friends = Friend.objects.filter(user=user)
        return Response(
            self.serializer_class(all_friends, many=True).data,
            status=status.HTTP_200_OK,
        )


class AcceptUserRequest(CreateAPIView):
    queryset = RequestToFriend.objects.all()
    serializer_class = RequestToFriendSerializer
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        """
        accept incoming friend request
        """
        if isinstance(request.user, AnonymousUser):
            return Response({'Error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        validated = self.serializer_class().validate_friend(request.data.copy())

        if 'friend' not in validated:
            return Response(
                {
                    'Error': 'friend is required field',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend = User.objects.get(username=validated['friend'])
        except User.DoesNotExist:
            return Response({'Error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = self.queryset.get(
                Q(receiver=request.user.id) & Q(inviter=friend.id) & Q(status=False),
            )
        except RequestToFriend.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        add_friend = Friend.objects.filter(user=request.user, friend=friend)
        if add_friend.exists():
            return Response({'error': 'already approved'}, status=status.HTTP_400_BAD_REQUEST)

        add_friend.create(
            user=request.user,
            friend=friend,
        )

        data.delete()

        return Response({'Success': 'request is accepted'}, status=status.HTTP_200_OK)


class DestroyFriend(DestroyAPIView):
    """
    delete friend from user friend
    """
    queryset = Friend.objects.all()
    serializer_class = UserFriendSerializer
    authentication_classes = (authentication.JWTAuthentication,)

    def delete(self, request, *args, **kwargs):

        if isinstance(request.user, AnonymousUser):
            return Response({'Error': 'not access'}, status=status.HTTP_401_UNAUTHORIZED)

        validated = self.serializer_class().validate_friend(request.data.copy())

        if 'friend' not in validated:
            return Response(
                {
                    'Error': 'friend is required field',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            friend = User.objects.get(username=validated['friend'])
        except User.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        data = self.queryset.filter(user=request.user, friend=friend.id)

        if not data.exists():
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        data.delete()

        return Response({'success': 'user deleted'}, status=status.HTTP_200_OK)
