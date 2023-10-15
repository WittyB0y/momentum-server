import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_send_to_yourself_friend_request(client, user_registration):
    username, password = user_registration['username'], user_registration['password']
    token = dict(client.post(reverse('token_obtain_pair'), {
        'username': username,
        'password': password,
    }).json())['access']
    response = client.post(reverse('add_friend'), headers={'Authorization': f'Bearer {token}'},
                           data={'friend': f'{username}'})
    assert dict(response.json())['Error'] == 'you can not add yourself to friend'
    assert response.status_code == 400


@pytest.mark.django_db
def test_send_to_friend_request_to_username_not_found(client, user_registration):
    username, password = user_registration['username'], user_registration['password']
    token = dict(client.post(reverse('token_obtain_pair'), {
        'username': username,
        'password': password,
    }).json())['access']
    response = client.post(reverse('add_friend'), headers={'Authorization': f'Bearer {token}'},
                           data={'friend': 'test123Test123'})
    assert response.status_code == 404
    assert dict(response.json())['Error'] == 'user not found'


@pytest.mark.django_db
def test_add_success_to_friend_and_repeat_request(client, user_registration, user_registration2):
    username1, password1 = user_registration['username'], user_registration['password']
    username2 = user_registration2['username']
    token = dict(client.post(reverse('token_obtain_pair'), {
        'username': username1,
        'password': password1,
    }).json())['access']
    response = client.post(reverse('add_friend'), headers={'Authorization': f'Bearer {token}'},
                           data={'friend': username2})
    assert response.status_code == 200
    assert dict(response.json())['Success'] == 'request sent'
    response = client.post(reverse('add_friend'), headers={'Authorization': f'Bearer {token}'},
                           data={'friend': username2})
    assert dict(response.json())['Warning'] == 'request already sent'
    assert response.status_code == 202
