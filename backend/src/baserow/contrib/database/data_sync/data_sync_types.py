from typing import Dict, List

import advocate
from advocate.exceptions import UnacceptableAddressException
from icalendar import Calendar
from requests.exceptions import RequestException

from baserow.contrib.database.fields.models import DateField, TextField

from .exceptions import SyncError
from .models import ICalCalendarDataSync
from .registries import DataSyncProperty, DataSyncType


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
                "dtstart": component.get("dtstart").dt,
                "dtend": component.get("dtend").dt,
                "summary": str(component.get("summary")),
            }
            for component in calendar.walk()
            if component.name == "VEVENT"
        ]
