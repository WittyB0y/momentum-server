import pytest
from django.contrib.auth.models import User
from django.urls import reverse


def do_post_request(client, name, **kwargs):
    return client.post(reverse(name), kwargs)


@pytest.mark.django_db
def test_success_user_registration(client):
    username = 'test123'
    password = 'Test123@'
    email = "test@text.com"
    first_name = 'Test'
    response = do_post_request(
        client,
        'register',
        username=username,
        password=password,
        email=email,
        first_name=first_name,
    )
    response_data = {
        "username": username.capitalize(),
        "email": email.capitalize(),
        "first_name": first_name.capitalize(),
    }

    assert response.status_code == 200
    assert response.json() == response_data
    assert User.objects.filter(username=username.capitalize()).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, email, first_name, excepted', [(
        '3@4SDfsdF',
        'testTest@12',
        'test@icloud.com',
        'Test',
        {
            'code': 400,
            'msg': {
                "non_field_errors": [
                    "Incorrect username."
                ]
            },
        },
), (
        'd',
        'testTest@12',
        'test@icloud.com',
        'Test',
        {
            'code': 400,
            'msg': {
                "non_field_errors": [
                    "Incorrect username."
                ]
            },
        },
), (
        'Test12334',
        'asfgf',
        'test@icloud.com',
        'Test',
        {
            'code': 400,
            'msg': {
                "non_field_errors": [
                    "Incorrect password."
                ]
            },
        },
), (
        'TestT123tT',
        'asd123ASD@',
        'qwe@df',
        'Test',
        {
            'code': 400,
            'msg': {
                "email": [
                    "Enter a valid email address."
                ]
            },
        },
), (
        'Tester234',
        'asdAS123@',
        'test@icl.com',
        '123',
        {
            'code': 400,
            'msg': {
                "non_field_errors": [
                    "Incorrect first_name."
                ]
            },
        },
), (
        '',
        '',
        '',
        '',
        {
            'code': 400,
            'msg': {
                "username": [
                    "This field may not be blank."
                ],
                "email": [
                    "This field may not be blank."
                ],
                "password": [
                    "This field may not be blank."
                ],
            },
        }
),
]
                         )
def test_fail_user_registration_incorrect_fields(
        client,
        username,
        password,
        email,
        first_name,
        excepted,
):
    response = do_post_request(
        client,
        'register',
        username=username,
        password=password,
        email=email,
        first_name=first_name,
    )

    assert response.status_code == excepted['code']
    assert response.json() == excepted['msg']
    assert not User.objects.filter(username=username.capitalize()).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, email, first_name, excepted', [
    (
            'testTestTester' * 50,
            '123ASD@Ds',
            'test@test.com',
            'Test',
            {
                'code': 400,
                'msg': {
                    "username": [
                        "Ensure this field has no more than 150 characters."
                    ]
                },
            },
    ), (
            'test123WERsd',
            '123ASD@Dsdf' * 50,
            'test@test.com',
            'Test',
            {
                'code': 400,
                'msg': {
                    "password": [
                        "Ensure this field has no more than 128 characters."
                    ]
                }
            },
    ), (
            'test123WERsd1',
            '123ASD@Dsdf',
            f'{"testtest" * 100}@{"test" * 100}.com',
            'Test',
            {
                'code': 400,
                'msg': {
                    "email": [
                        "Ensure this field has no more than 500 characters.",
                        "Enter a valid email address."
                    ]
                }
            },
    ), (
            'test123WERsd1',
            '123ASD@Dsdf',
            'tester12345@test.com',
            f'Test{"TEST" * 50}',
            {
                'code': 400,
                'msg': {
                    "first_name": [
                        "Ensure this field has no more than 150 characters."
                    ]
                }
            },
    ),
])
def test_fail_user_registration_max_value_fields(
        client,
        username,
        password,
        email,
        first_name,
        excepted,
):
    response = do_post_request(
        client,
        'register',
        username=username,
        password=password,
        email=email,
        first_name=first_name,
    )
    assert response.status_code == excepted['code']
    assert response.json() == excepted['msg']
    assert not User.objects.filter(username=username.capitalize()).exists()
