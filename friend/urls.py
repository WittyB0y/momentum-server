from django.urls import path

from friend.views import RequestToAddFriend, GetAllUserFriend, AcceptUserRequest, DestroyFriend

urlpatterns = [
    path('follow/', RequestToAddFriend.as_view(), name='add_friend'),
    path('follow/accept/', AcceptUserRequest.as_view(), name='accept_friend_request'),
    path('delete/', DestroyFriend.as_view(), name='destroy_friend'),
    path('my/', GetAllUserFriend.as_view(), name='my_friends'),
]
