from django.urls import reverse

import pytest
import responses
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from baserow.contrib.database.data_sync.models import DataSync, DataSyncProperty

ICAL_FEED_WITH_ONE_ITEMS = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ical.marudot.com//iCal Event Maker
X-WR-CALNAME:Test feed
NAME:Test feed
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/Berlin
LAST-MODIFIED:20231222T233358Z
TZURL:https://www.tzurl.org/zoneinfo-outlook/Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZNAME:CEST
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZNAME:CET
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
DTSTAMP:20240901T195538Z
UID:1725220374375-34056@ical.marudot.com
DTSTART;TZID=Europe/Berlin:20240901T100000
DTEND;TZID=Europe/Berlin:20240901T110000
SUMMARY:Test event 0
URL:https://baserow.io
DESCRIPTION:Test description 1
LOCATION:Amsterdam
END:VEVENT
END:VCALENDAR"""


@pytest.mark.django_db
def test_create_data_sync_no_permissions(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table()

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "ical_calendar",
            "visible_properties": ["uid", "dtstart", "dtend", "summary"],
            "ical_url": "https://baserow.io/ical.ics",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_create_data_sync_invalid_type(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table(user=user)

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "test",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert response_json["detail"]["type"][0]["code"] == "invalid_choice"


@pytest.mark.django_db
def test_create_data_sync_wrong_properties(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table(user=user)

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "ical_calendar",
            "visible_properties": ["TEST"],
            "ical_url": "https://baserow.io/ical.ics",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_PROPERTY_NOT_FOUND"
    assert "TEST" in response_json["detail"]


@pytest.mark.django_db
def test_create_data_sync_invalid_polymorphic_property(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table(user=user)

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "ical_calendar",
            "visible_properties": ["uid"],
            "ical_url": "test",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"


@pytest.mark.django_db
@responses.activate
def test_create_data_sync(data_fixture, api_client):
    responses.add(
        responses.GET,
        "https://baserow.io/ical.ics",
        status=200,
        body=ICAL_FEED_WITH_ONE_ITEMS,
    )

    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table(user=user)

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "ical_calendar",
            "visible_properties": ["uid", "dtstart", "dtend", "summary"],
            "ical_url": "https://baserow.io/ical.ics",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    data_syncs = list(DataSync.objects.all())
    assert len(data_syncs) == 1
    data_sync = data_syncs[0]

    properties = DataSyncProperty.objects.filter(data_sync=data_sync).order_by("id")

    assert response.json() == {
        "id": data_sync.table_id,
        "name": "Test 1",
        "order": 1,
        "database_id": database.id,
        "data_sync": {
            "id": data_sync.id,
            "data_sync_properties": [
                {"field_id": properties[0].field_id, "key": "uid"},
                {"field_id": properties[1].field_id, "key": "dtstart"},
                {"field_id": properties[2].field_id, "key": "dtend"},
                {"field_id": properties[3].field_id, "key": "summary"},
            ],
            "last_sync": None,
        },
    }


@pytest.mark.django_db
@pytest.mark.undo_redo
@responses.activate
def test_can_undo_redo_create_data_sync(api_client, data_fixture):
    same_session_id = "test"

    responses.add(
        responses.GET,
        "https://baserow.io/ical.ics",
        status=200,
        body=ICAL_FEED_WITH_ONE_ITEMS,
    )

    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_table(user=user)

    url = reverse("api:database:data_sync:list", kwargs={"database_id": database.id})
    response = api_client.post(
        url,
        {
            "table_name": "Test 1",
            "type": "ical_calendar",
            "visible_properties": ["uid", "dtstart", "dtend", "summary"],
            "ical_url": "https://baserow.io/ical.ics",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
        HTTP_CLIENTSESSIONID=same_session_id,
    )
    assert response.status_code == HTTP_200_OK

    data_sync = DataSync.objects.all().first()

    api_client.patch(
        reverse("api:user:undo"),
        {
            "scopes": {
                "table": data_sync.table_id,
                "application": data_sync.table.database_id,
            }
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
        HTTP_CLIENTSESSIONID=same_session_id,
    )
    assert response.status_code == HTTP_200_OK

    data_sync.table.refresh_from_db()
    assert data_sync.table.trashed is True

    api_client.patch(
        reverse("api:user:redo"),
        {
            "scopes": {
                "table": data_sync.table_id,
                "application": data_sync.table.database_id,
            }
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
        HTTP_CLIENTSESSIONID=same_session_id,
    )
    assert response.status_code == HTTP_200_OK

    data_sync.table.refresh_from_db()
    assert data_sync.table.trashed is False
