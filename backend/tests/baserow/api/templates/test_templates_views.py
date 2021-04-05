import pytest

from rest_framework.status import HTTP_200_OK

from django.shortcuts import reverse


@pytest.mark.django_db
def test_list_templates(api_client, data_fixture):
    category_1 = data_fixture.create_template_category(name='Cat 1')
    category_3 = data_fixture.create_template_category(name='Cat 3')
    category_2 = data_fixture.create_template_category(name='Cat 2')

    template_1 = data_fixture.create_template(
        name='Template 1',
        icon='document',
        category=category_1,
    )
    template_2 = data_fixture.create_template(
        name='Template 2',
        icon='document',
        category=category_2,
    )
    template_3 = data_fixture.create_template(
        name='Template 3',
        icon='document',
        categories=[category_2, category_3]
    )

    response = api_client.get(reverse('api:templates:list'))
    assert response.status_code == HTTP_200_OK
    response_json = response.json()

    assert len(response_json) == 3
    assert response_json[0]['id'] == category_1.id
    assert response_json[0]['name'] == 'Cat 1'
    assert len(response_json[0]['templates']) == 1
    assert response_json[0]['templates'][0]['id'] == template_1.id
    assert response_json[0]['templates'][0]['name'] == template_1.name
    assert response_json[0]['templates'][0]['icon'] == template_1.icon
    assert response_json[0]['templates'][0]['group_id'] == template_1.group_id
    assert len(response_json[1]['templates']) == 2
    assert response_json[1]['templates'][0]['id'] == template_2.id
    assert response_json[1]['templates'][1]['id'] == template_3.id
    assert len(response_json[2]['templates']) == 1
    assert response_json[2]['templates'][0]['id'] == template_3.id
