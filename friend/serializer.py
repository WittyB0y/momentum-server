from rest_framework import serializers

from friend.models import Friend
from photo.serializer import UserAvatarSerializer
from user.serializers import GetUserSerializer


class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'friend', 'dataAdded',)

    def save(self, *args, **kwargs):
        user_friend = Friend(
            user=self.validated_data['user'],
            friend=self.validated_data['friend'],
        )
        user_friend.save()
        return user_friend


class GetAllUserFriendSerializer(serializers.ModelSerializer):
    friend_photo = UserAvatarSerializer(source='friend.useravatar', read_only=True)
    friend = GetUserSerializer()

    class Meta:
        model = Friend
        fields = ('friend_photo', 'friend', 'dataAdded', )
