import pytest
from django.contrib.auth.models import User
from rest_framework.reverse import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('username, excepted', [
    (
            '123124',
            {
                'code': 404,
                'msg': {
                    "IsExist": False,
                },
            },
    ), (
            '1test1test2',
            {
                'code': 404,
                'msg': {
                    "IsExist": False,
                },
            },
    ), (
            'estrester123321',
            {
                'code': 404,
                'msg': {
                    "IsExist": False,
                },
            },
    ),
])
def test_check_free_username(client, username, excepted):
    response = client.get(reverse('check_is_available_username'), {'username': username})
    assert response.json() == excepted['msg']
    assert response.status_code == excepted['code']
    assert not User.objects.filter(username=username.capitalize()).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('username, excepted', [
    (
            'rtr ffg fg',
            {
                'code': 400,
                'msg': {
                    "username": [
                        "Incorrect username."
                    ]
                }
            },
    ), (
            '#FDsa12',
            {
                'code': 400,
                'msg': {
                    "username": [
                        "Incorrect username."
                    ]
                },
            },
    ),
])
def test_check_incorrect_username(client, username, excepted):
    response = client.get(reverse('check_is_available_username'), {'username': username})
    assert response.json() == excepted['msg']
    assert response.status_code == excepted['code']
    assert not User.objects.filter(username=username.capitalize()).exists()


@pytest.mark.django_db
def test_user_exists(client, client_with_user):
    response = client.get(
        reverse('check_is_available_username'),
        {
            'username': client_with_user.username,
        },
    )
    assert response.json() == {
                    "IsExist": True,
                }
    assert response.status_code == 200
    assert User.objects.filter(username=client_with_user.username).exists()
