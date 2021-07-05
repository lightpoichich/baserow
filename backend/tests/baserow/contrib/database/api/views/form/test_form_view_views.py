import pytest

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from django.shortcuts import reverse

from baserow.contrib.database.views.models import FormView


@pytest.mark.django_db
def test_create_form_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    user_file_1 = data_fixture.create_user_file()
    user_file_2 = data_fixture.create_user_file()

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {
            "name": "Test Form",
            "type": "form",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["slug"]) == 36
    assert response_json["type"] == "form"
    assert response_json["name"] == "Test Form"
    assert response_json["table_id"] == table.id
    assert response_json["public"] is False
    assert response_json["password"] == ""
    assert response_json["title"] == ""
    assert response_json["description"] == ""
    assert response_json["cover_image"] is None
    assert response_json["logo_image"] is None
    assert response_json["submit_action"] == "MESSAGE"
    assert response_json["submit_action_redirect_url"] == ""
    assert response_json["submit_email_confirmation"] == ""

    form = FormView.objects.all()[0]
    assert response_json["id"] == form.id
    assert response_json["name"] == form.name
    assert response_json["order"] == form.order
    assert response_json["slug"] == str(form.slug)
    assert form.table_id == table.id
    assert form.public is False
    assert form.password == ""
    assert form.title == ""
    assert form.description == ""
    assert form.cover_image is None
    assert form.logo_image is None
    assert form.submit_action == "MESSAGE"
    assert form.submit_action_redirect_url == ""
    assert form.submit_email_confirmation == ""
    assert "filters" not in response_json
    assert "sortings" not in response_json

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {
            "slug": "Test",
            "name": "Test Form 2",
            "type": "form",
            "public": True,
            "password": "test",
            "title": "Title",
            "description": "Description",
            "cover_image": {"name": user_file_1.name},
            "logo_image": {"name": user_file_2.name},
            "submit_action": "REDIRECT",
            "submit_action_redirect_url": "https://localhost",
            "submit_email_confirmation": "bram@test.nl",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["slug"] != "Test"
    assert response_json["name"] == "Test Form 2"
    assert response_json["type"] == "form"
    assert response_json["public"] is True
    assert response_json["password"] == "test"
    assert response_json["title"] == "Title"
    assert response_json["description"] == "Description"
    assert response_json["cover_image"]["name"] == user_file_1.name
    assert response_json["logo_image"]["name"] == user_file_2.name
    assert response_json["submit_action"] == "REDIRECT"
    assert response_json["submit_action_redirect_url"] == "https://localhost"
    assert response_json["submit_email_confirmation"] == "bram@test.nl"

    form = FormView.objects.all()[1]
    assert form.name == "Test Form 2"
    assert form.order == 2
    assert form.table == table
    assert form.public is True
    assert form.password == "test"
    assert form.title == "Title"
    assert form.description == "Description"
    assert form.cover_image_id == user_file_1.id
    assert form.logo_image_id == user_file_2.id
    assert form.submit_action == "REDIRECT"
    assert form.submit_action_redirect_url == "https://localhost"
    assert form.submit_email_confirmation == "bram@test.nl"

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {
            "type": "form",
            "name": "Test",
            "cover_image": None,
            "logo_image": {"name": user_file_2.name},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["cover_image"] is None
    assert response_json["logo_image"]["name"] == user_file_2.name


@pytest.mark.django_db
def test_update_form_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    view = data_fixture.create_form_view(table=table)
    user_file_1 = data_fixture.create_user_file()
    user_file_2 = data_fixture.create_user_file()

    url = reverse("api:database:views:item", kwargs={"view_id": view.id})
    response = api_client.patch(
        url,
        {
            "slug": "test",
            "name": "Test Form 2",
            "type": "form",
            "public": True,
            "password": "test",
            "title": "Title",
            "description": "Description",
            "cover_image": {"name": user_file_1.name},
            "logo_image": {"name": user_file_2.name},
            "submit_action": "REDIRECT",
            "submit_action_redirect_url": "https://localhost",
            "submit_email_confirmation": "bram@test.nl",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["slug"] != "test"
    assert response_json["slug"] == str(view.slug)
    assert response_json["name"] == "Test Form 2"
    assert response_json["type"] == "form"
    assert response_json["public"] is True
    assert response_json["password"] == "test"
    assert response_json["title"] == "Title"
    assert response_json["description"] == "Description"
    assert response_json["cover_image"]["name"] == user_file_1.name
    assert response_json["logo_image"]["name"] == user_file_2.name
    assert response_json["submit_action"] == "REDIRECT"
    assert response_json["submit_action_redirect_url"] == "https://localhost"
    assert response_json["submit_email_confirmation"] == "bram@test.nl"

    form = FormView.objects.all()[0]
    assert form.name == "Test Form 2"
    assert form.table == table
    assert form.public is True
    assert form.password == "test"
    assert form.title == "Title"
    assert form.description == "Description"
    assert form.cover_image_id == user_file_1.id
    assert form.logo_image_id == user_file_2.id
    assert form.submit_action == "REDIRECT"
    assert form.submit_action_redirect_url == "https://localhost"
    assert form.submit_email_confirmation == "bram@test.nl"

    url = reverse("api:database:views:item", kwargs={"view_id": view.id})
    response = api_client.patch(
        url,
        {
            "cover_image": {"name": user_file_2.name},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["cover_image"]["name"] == user_file_2.name
    assert response_json["logo_image"]["name"] == user_file_2.name

    url = reverse("api:database:views:item", kwargs={"view_id": view.id})
    response = api_client.patch(
        url,
        {
            "cover_image": None,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    print(response_json)
    assert response.status_code == HTTP_200_OK
    assert response_json["cover_image"] is None
    assert response_json["logo_image"]["name"] == user_file_2.name


@pytest.mark.django_db
def test_rotate_slug(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    view = data_fixture.create_form_view(table=table)
    view_2 = data_fixture.create_form_view()
    old_slug = str(view.slug)

    url = reverse("api:database:views:form:rotate_slug", kwargs={"view_id": view_2.id})
    response = api_client.post(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"

    url = reverse("api:database:views:form:rotate_slug", kwargs={"view_id": 99999})
    response = api_client.post(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_404_NOT_FOUND

    url = reverse("api:database:views:form:rotate_slug", kwargs={"view_id": view.id})
    response = api_client.post(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["slug"] != old_slug
    assert len(response_json["slug"]) == 36


@pytest.mark.django_db
def test_meta_submit_form_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    user_2, token_2 = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    user_file_1 = data_fixture.create_user_file()
    user_file_2 = data_fixture.create_user_file()
    form = data_fixture.create_form_view(
        table=table,
        title="Title",
        description="Description",
        cover_image=user_file_1,
        logo_image=user_file_2,
    )
    text_field = data_fixture.create_text_field(table=table)
    number_field = data_fixture.create_number_field(table=table)
    disabled_field = data_fixture.create_text_field(table=table)
    data_fixture.create_form_view_field_option(
        form,
        text_field,
        name="Text field title",
        description="Text field description",
        required=True,
        enabled=True,
        order=1,
    )
    data_fixture.create_form_view_field_option(
        form, number_field, required=False, enabled=True, order=2
    )
    data_fixture.create_form_view_field_option(
        form, disabled_field, required=False, enabled=False, order=3
    )

    url = reverse("api:database:views:form:submit", kwargs={"slug": "NOT_EXISTING"})
    response = api_client.get(url, format="json")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.get(url, format="json")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token_2}")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK

    form.public = True
    form.save()

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.get(url, format="json")
    assert response.status_code == HTTP_200_OK
    response_json = response.json()

    assert response_json["title"] == "Title"
    assert response_json["description"] == "Description"
    assert response_json["cover_image"]["name"] == user_file_1.name
    assert response_json["logo_image"]["name"] == user_file_2.name
    assert len(response_json["fields"]) == 2
    assert response_json["fields"][0] == {
        "name": "Text field title",
        "description": "Text field description",
        "required": True,
        "order": 1,
        "field": {"id": text_field.id, "type": "text", "text_default": ""},
    }
    assert response_json["fields"][1] == {
        "name": number_field.name,
        "description": "",
        "required": False,
        "order": 2,
        "field": {
            "id": number_field.id,
            "type": "number",
            "number_type": "INTEGER",
            "number_decimal_places": 1,
            "number_negative": False,
        },
    }


@pytest.mark.django_db
def test_submit_form_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    user_2, token_2 = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    form = data_fixture.create_form_view(
        table=table,
        submit_action_message="Test",
        submit_action_redirect_url="https://baserow.io",
    )
    text_field = data_fixture.create_text_field(table=table)
    number_field = data_fixture.create_number_field(table=table)
    disabled_field = data_fixture.create_text_field(table=table)
    data_fixture.create_form_view_field_option(
        form, text_field, required=True, enabled=True, order=1
    )
    data_fixture.create_form_view_field_option(
        form, number_field, required=False, enabled=True, order=2
    )
    data_fixture.create_form_view_field_option(
        form, disabled_field, required=False, enabled=False, order=3
    )

    url = reverse("api:database:views:form:submit", kwargs={"slug": "NOT_EXISTING"})
    response = api_client.post(url, {}, format="json")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(url, {}, format="json")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url, {}, format="json", HTTP_AUTHORIZATION=f"JWT" f" {token_2}"
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_FORM_DOES_NOT_EXIST"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {
            # We do not provide the text field value, but that one is required and we
            # provide a wrong value for the number field, so we expect two errors.
            f"field_{number_field.id}": {},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT" f" {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert len(response_json["detail"]) == 2
    assert response_json["detail"][f"field_{text_field.id}"][0]["code"] == "required"
    assert response_json["detail"][f"field_{number_field.id}"][0]["code"] == "invalid"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {
            f"field_{text_field.id}": "Valid",
            f"field_{number_field.id}": 0,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT" f" {token}",
    )
    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json == {
        "submit_action": "MESSAGE",
        "submit_action_message": "Test",
        "submit_action_redirect_url": "https://baserow.io",
    }

    model = table.get_model()
    all = model.objects.all()
    assert len(all) == 1
    assert getattr(all[0], f"field_{text_field.id}") == "Valid"
    assert getattr(all[0], f"field_{number_field.id}") == 0

    form.public = True
    form.save()

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {},
        format="json",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert len(response_json["detail"]) == 1
    assert response_json["detail"][f"field_{text_field.id}"][0]["code"] == "required"

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {
            f"field_{text_field.id}": "A value",
            f"field_{disabled_field.id}": "Value",
        },
        format="json",
    )
    assert response.status_code == HTTP_200_OK

    model = table.get_model()
    all = model.objects.all()
    assert len(all) == 2
    assert getattr(all[1], f"field_{text_field.id}") == "A value"
    assert getattr(all[1], f"field_{number_field.id}") is None
    assert getattr(all[1], f"field_{disabled_field.id}") is None

    date_field = data_fixture.create_date_field(table=table)
    file_field = data_fixture.create_file_field(table=table)
    url_field = data_fixture.create_url_field(table=table)
    single_select_field = data_fixture.create_single_select_field(table=table)
    boolean_field = data_fixture.create_boolean_field(table=table)
    phone_field = data_fixture.create_phone_number_field(table=table)
    data_fixture.create_form_view_field_option(
        form, file_field, required=True, enabled=True
    )
    data_fixture.create_form_view_field_option(
        form, url_field, required=True, enabled=True
    )
    data_fixture.create_form_view_field_option(
        form, single_select_field, required=True, enabled=True
    )
    data_fixture.create_form_view_field_option(
        form, boolean_field, required=True, enabled=True
    )
    data_fixture.create_form_view_field_option(
        form, date_field, required=True, enabled=True
    )
    data_fixture.create_form_view_field_option(
        form, phone_field, required=True, enabled=True
    )

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {
            f"field_{text_field.id}": "",
            f"field_{date_field.id}": None,
            f"field_{file_field.id}": [],
            f"field_{url_field.id}": "",
            f"field_{single_select_field.id}": "",
            f"field_{boolean_field.id}": False,
            f"field_{phone_field.id}": "",
        },
        format="json",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert len(response_json["detail"]) == 7

    url = reverse("api:database:views:form:submit", kwargs={"slug": form.slug})
    response = api_client.post(
        url,
        {},
        format="json",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert len(response_json["detail"]) == 7
