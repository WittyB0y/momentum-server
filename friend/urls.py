from django.urls import path

from friend.views import UserFriend, GetAllUserFriend

urlpatterns = [
    path('add/', UserFriend.as_view(), name='add_friend'),
    path('my/', GetAllUserFriend.as_view(), name='my_friends'),
]
