from django.contrib.auth import get_user_model
from django.db import models

from baserow.contrib.automation.models import Trigger, UserAction
from baserow.contrib.database.models import Table
from baserow.core.models import Connection

User = get_user_model()


class InternalBaserowConnection(Connection):
    authorized_user = models.ForeignKey(User, on_delete=models.CASCADE)


class ExternalBaserowConnection(Connection):
    api_key = models.CharField(max_length=255)
    baserow_url = models.URLField()


class BaserowRowCreatedTrigger(Trigger):
    table = models.ForeignKey(
        Table,
        related_name="baserow_row_created_triggers",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class BaserowListRowsUserAction(UserAction):
    table = models.ForeignKey(
        Table,
        related_name="baserow_list_rows_user_actions",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class BaserowGetRowUserAction(UserAction):
    table = models.ForeignKey(
        Table,
        related_name="baserow_get_row_user_actions",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    row_id = models.IntegerField(
        null=True,
        default=None,
    )
