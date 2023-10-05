from django.urls import path

from friend.views import RequestToAddFriend, GetAllUserFriend

urlpatterns = [
    path('add/', RequestToAddFriend.as_view(), name='add_friend'),
    path('my/', GetAllUserFriend.as_view(), name='my_friends'),
]
