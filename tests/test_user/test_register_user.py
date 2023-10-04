import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_success_user_registration(client):
    username = 'TestUser123'
    password = 'TestPassword'
    email = "Test@test123.test"
    first_name = 'Test1'
    last_name = 'Tester'
    response = client.post(reverse('register'), {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    })
    response_data = {
        "username": username,
        "email": email,
        "first_name": first_name
    }

    assert response.status_code == 200
    assert response.json() == response_data
    assert User.objects.filter(username=username).exists()


@pytest.mark.django_db
def test_fail_user_registration_empty_field(client):
    username = ''
    password = ''
    email = ''
    first_name = ''
    last_name = ''

    response = client.post(reverse('register'), {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    })
    response_data = {
        "username": [
            "This field may not be blank."
        ],
        "password": [
            "This field may not be blank."
        ],
    }

    assert response.json() == response_data
    assert not User.objects.filter(username=username).exists()
