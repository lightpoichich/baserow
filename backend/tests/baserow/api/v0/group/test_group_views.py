import pytest

from django.shortcuts import reverse

from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@pytest.mark.django_db
def test_list_groups(client, data_fixture, django_assert_num_queries):
    user = data_fixture.create_user(email='test@test.nl', password='password',
                                    first_name='Test1')
    group_2 = data_fixture.create_user_group(user=user, order=2)
    group_1 = data_fixture.create_user_group(user=user, order=1)

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    with django_assert_num_queries(4):
        response = client.get(reverse('api_v0:groups:list'), **{
            'HTTP_AUTHORIZATION': f'JWT {token}'
        })
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['id'] == group_1.id
        assert response_json[0]['order'] == 1
        assert response_json[1]['id'] == group_2.id
        assert response_json[1]['order'] == 2
