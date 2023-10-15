import pytest
from django.contrib.auth.models import User
from rest_framework.reverse import reverse


class RefreshTokenError(Exception):
    ...


REFRESH_TOKEN = None


@pytest.mark.django_db
def test_get_token_success(client, user_registration):
    obj = user_registration
    username = obj['username']
    password = obj['password']
    response = client.post(
        reverse('token_obtain_pair'), {
            'username': username,
            'password': password,
        }
    )
    assert 'refresh' in response.json()
    assert 'access' in response.json()

    assert User.objects.filter(username=username.capitalize()).exists()

    refresh = dict(response.json())['refresh']
    global REFRESH_TOKEN
    if not REFRESH_TOKEN:
        REFRESH_TOKEN = refresh
    return refresh


@pytest.mark.django_db
def test_refresh_token_success(client):
    global REFRESH_TOKEN
    if not REFRESH_TOKEN:
        raise RefreshTokenError('The value REFRESH_TOKEN does not assign.')
    response = client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'AsdasdTest1234',
            'password': 'fdgfSD23!',
        }
    )
    assert 'refresh' not in response.json()
    assert 'access' not in response.json()
    assert response.status_code == 401
    assert not User.objects.filter(username='AsdasdTest1234').exists()


def test_get_token_fail(client):
    response = client.post(reverse('token_refresh'), {'refresh': REFRESH_TOKEN})

    assert len(dict(response.json())) == 1
    assert 'access' in dict(response.json())
    assert 'refresh' not in dict(response.json())


@pytest.mark.django_db
def test_get_refresh_token_fail(client):
    response = client.post(
        reverse('token_obtain_pair'),
        {
            'username': '11111111Art',
            'password': 'TestPass123@',
        }
    )
    assert dict(response.json()) == {'detail': 'No active account found with the given credentials'}
