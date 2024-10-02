from datetime import date, datetime, timezone
from typing import Any, Dict, List

import advocate
from advocate.exceptions import UnacceptableAddressException
from icalendar import Calendar
from requests.exceptions import RequestException

from baserow.contrib.database.fields.models import DateField, TextField

from .exceptions import SyncError
from .models import ICalCalendarDataSync
from .registries import DataSyncProperty, DataSyncType


def normalize_datetime(d):
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    else:
        d = d.astimezone(timezone.utc)

    d = d.replace(second=0, microsecond=0)
    return d


def normalize_date(d):
    if isinstance(d, datetime):
        d = d.date()
    return d


def compare_date(date1, date2):
    if isinstance(date1, datetime) and isinstance(date2, datetime):
        date1 = normalize_datetime(date1)
        date2 = normalize_datetime(date2)
    elif isinstance(date1, date) or isinstance(date2, date):
        date1 = normalize_date(date1)
        date2 = normalize_date(date2)
    return date1 == date2


class UIDICalCalendarDataSyncProperty(DataSyncProperty):
    unique_primary = True
    immutable_properties = True

    def to_baserow_field(self) -> TextField:
        return TextField(name=self.name)


class DateStartICalCalendarDataSyncProperty(DataSyncProperty):
    immutable_properties = False

    def to_baserow_field(self) -> DateField:
        return DateField(
            name=self.name,
            date_format="ISO",
            date_include_time=True,
            date_time_format="24",
            date_show_tzinfo=True,
        )

    def is_equal(self, baserow_row_value: Any, data_sync_row_value: Any) -> bool:
        return compare_date(baserow_row_value, data_sync_row_value)


class DateEndICalCalendarDataSyncProperty(DataSyncProperty):
    immutable_properties = False

    def to_baserow_field(self) -> DateField:
        return DateField(
            name=self.name,
            date_format="ISO",
            date_include_time=True,
            date_time_format="24",
            date_show_tzinfo=True,
        )

    def is_equal(self, baserow_row_value: Any, data_sync_row_value: Any) -> bool:
        return compare_date(baserow_row_value, data_sync_row_value)


class SummaryICalCalendarDataSyncProperty(DataSyncProperty):
    immutable_properties = True

    def to_baserow_field(self) -> TextField:
        return TextField(name=self.name)


class ICalCalendarDataSyncType(DataSyncType):
    type = "ical_calendar"
    model_class = ICalCalendarDataSync
    allowed_fields = ["ical_url"]
    serializer_field_names = ["ical_url"]

    def get_properties(self, instance) -> List[DataSyncProperty]:
        return [
            UIDICalCalendarDataSyncProperty("uid", "Unique ID"),
            DateStartICalCalendarDataSyncProperty("dtstart", "Start date"),
            DateEndICalCalendarDataSyncProperty("dtend", "End date"),
            SummaryICalCalendarDataSyncProperty("summary", "Summary"),
        ]

    def get_all_rows(self, instance) -> List[Dict]:
        try:
            response = advocate.get(instance.ical_url, timeout=10)
        except (RequestException, UnacceptableAddressException, ConnectionError):
            raise SyncError("The provided URL could not be reached.")

        if not response.ok:
            raise SyncError(
                "The request to the URL didn't respond with an OK response code."
            )

        try:
            calendar = Calendar.from_ical(response.content)
        except ValueError as e:
            raise SyncError(f"Could not read calendar file: {str(e)}")

        return [
            {
                "uid": str(component.get("uid")),
                "dtstart": getattr(component.get("dtstart"), "dt", None),
                "dtend": getattr(component.get("dtend"), "dt", None),
                "summary": str(component.get("summary") or ""),
            }
            for component in calendar.walk()
            if component.name == "VEVENT"
        ]
