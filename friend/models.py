from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    dataAdded = models.DateTimeField(auto_now_add=True)


class RequestToFriend(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter', null=False)
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        null=False,
    )
    status = models.BooleanField(default=False, null=False)
    sentRequestData = models.DateTimeField(auto_now_add=True)


class BlockList(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_blocklist',
        null=False,
    )
    blocked_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_user',
        null=False,
    )
