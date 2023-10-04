import pytest
from django.contrib.auth.models import User


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
        username="qtestuserq",
        first_name="Test",
        email="testuser@example.com",
        password="testpAssword123@"
    )
    user.save()
    return user
