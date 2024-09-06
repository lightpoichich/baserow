from django.contrib.contenttypes.models import ContentType
from django.db import models

from baserow.contrib.database.data_sync.registries import data_sync_type_registry
from baserow.contrib.database.fields.models import Field
from baserow.core.mixins import (
    CreatedAndUpdatedOnMixin,
    PolymorphicContentTypeMixin,
    WithRegistry,
)


class DataSync(
    CreatedAndUpdatedOnMixin,
    PolymorphicContentTypeMixin,
    models.Model,
    WithRegistry,
):
    table = models.ForeignKey(
        "database.Table",
        on_delete=models.CASCADE,
        null=True,
        related_name="data_syncs",
        help_text="The table where the data is synced into.",
    )
    last_sync = models.DateTimeField(
        null=True, help_text="Timestamp when the table was last synced."
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="data_syncs",
        on_delete=models.CASCADE,
    )
    properties = models.ManyToManyField(Field, through="DataSyncProperty")

    @staticmethod
    def get_type_registry():
        """Returns the registry related to this model class."""

        return data_sync_type_registry


class DataSyncProperty(models.Model):
    """
    An entry represents the visible property of the data sync table. If the entry
    doesn't exist, then the property is not visible as field in the table.
    """

    data_sync = models.ForeignKey(DataSync, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=255, help_text="The matching `key` of the `DataSyncProperty`."
    )


class ICalCalendarDataSync(DataSync):
    ical_url = models.URLField()
