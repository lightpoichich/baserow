import pytest

from django.contrib.auth import get_user_model
from django.shortcuts import reverse


User = get_user_model()


@pytest.mark.django_db
def test_create_user(client):
    response = client.post(reverse('api_v0:user:index'), {
        'name': 'Test1',
        'email': 'test@test.nl',
        'password': 'test12'
    }, format='json')

    assert response.status_code == 200
    user = User.objects.get(email='test@test.nl')
    assert user.first_name == 'Test1'
    assert user.email == 'test@test.nl'
    assert user.password != ''

    response_failed = client.post(reverse('api_v0:user:index'), {
        'name': 'Test1',
        'email': 'test@test.nl',
        'password': 'test12'
    }, format='json')

    assert response_failed.status_code == 400
    assert response_failed.json()['error'] == 'ERROR_EMAIL_ALREADY_EXISTS'

    response_failed_2 = client.post(reverse('api_v0:user:index'), {
        'email': 'test'
    }, format='json')

    assert response_failed_2.status_code == 400


@pytest.mark.django_db
def test_send_password_reset_email(data_fixture, client, mailoutbox):
    data_fixture.create_user(email='test@localhost')

    response = client.post(
        reverse('api_v0:user:send_password_reset_email'),
        {},
        format='json'
    )
    response_json = response.json()
    assert response.status_code == 400
    assert response_json['error'] == 'ERROR_REQUEST_BODY_VALIDATION'

    response = client.post(
        reverse('api_v0:user:send_password_reset_email'),
        {
            'email': 'unknown@localhost',
            'base_url': 'http://test.nl'
        },
        format='json'
    )
    assert response.status_code == 204
    assert len(mailoutbox) == 0

    response = client.post(
        reverse('api_v0:user:send_password_reset_email'),
        {
            'email': 'test@localhost',
            'base_url': 'http://test.nl'
        },
        format='json'
    )
    assert response.status_code == 204
    assert len(mailoutbox) == 1

    email = mailoutbox[0]
    assert 'test@localhost' in email.to
    assert email.body.index('http://test.nl')
