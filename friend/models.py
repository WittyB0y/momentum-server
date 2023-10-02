from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    dataAdded = models.DateTimeField(auto_now_add=True)
