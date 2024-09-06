from typing import Dict, List

import advocate
from icalendar import Calendar

from baserow.contrib.database.fields.models import DateField, TextField

from .models import ICalCalendarDataSync
from .registries import DataSyncProperty, DataSyncType


class UIDICalCalendarDataSyncProperty(DataSyncProperty):
    unique_primary = True

    def to_baserow_field(self) -> TextField:
        return TextField(name=self.name)


class DateStartICalCalendarDataSyncProperty(DataSyncProperty):
    def to_baserow_field(self) -> DateField:
        return DateField(
            name=self.name,
            date_format="ISO",
            date_include_time=True,
            date_time_format="24",
            date_show_tzinfo=True,
            date_force_timezone=False,
        )


class DateEndICalCalendarDataSyncProperty(DataSyncProperty):
    def to_baserow_field(self) -> DateField:
        return DateField(
            name=self.name,
            date_format="ISO",
            date_include_time=True,
            date_time_format="24",
            date_show_tzinfo=True,
            date_force_timezone=False,
        )


class SummaryICalCalendarDataSyncProperty(DataSyncProperty):
    def to_baserow_field(self) -> TextField:
        return TextField(name=self.name)


class ICalCalendarDataSyncType(DataSyncType):
    type = "ical_calendar"
    model_class = ICalCalendarDataSync
    allowed_fields = ["ical_url"]

    def get_properties(self, instance) -> List[DataSyncProperty]:
        return [
            UIDICalCalendarDataSyncProperty("uid", "Unique ID"),
            DateStartICalCalendarDataSyncProperty("dtstart", "Start date"),
            DateEndICalCalendarDataSyncProperty("dtend", "End date"),
            SummaryICalCalendarDataSyncProperty("summary", "Summary"),
        ]

    def get_all_rows(self, instance) -> List[Dict]:
        response = advocate.get(instance.ical_url, timeout=10)

        if not response.ok:
            raise Exception("@TODO custom exception")

        calendar = Calendar.from_ical(response.content)

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
