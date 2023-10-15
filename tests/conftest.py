import pytest
from django.contrib.auth.models import User
import enum

from tests.test_1_user.test_register_user import do_post_request


class UserData(enum.Enum):
    user1 = {
        "username": "Qtestuserq",
        "first_name": "Test",
        "email": "testuser@example.com",
        "password": "testpAssword123@",
    }


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    from django.conf import settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }


@pytest.fixture
def client_with_user(client):
    user = User.objects.create_user(
        username="Qtestuserq",
        first_name="Test",
        email="testuser@example.com",
        password="testpAssword123@"
    )
    user.save()
    return user


@pytest.fixture
def client_with_user2(client):
    user = User.objects.create_user(
        username="KotkaTestName",
        first_name="TestCat",
        email="catcattest@example.com",
        password="t123FGj23@"
    )
    user.save()
    return user


@pytest.fixture
def user_registration(client):
    username = 'Test123123'
    password = 'Test123@'
    email = "test@text.com"
    first_name = 'Test'
    do_post_request(
        client,
        'register',
        username=username,
        password=password,
        email=email,
        first_name=first_name,
    )
    return {'username': username, 'password': password}
