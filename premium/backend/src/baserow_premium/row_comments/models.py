from django.contrib.auth import get_user_model
from django.db import models

from baserow.contrib.database.table.models import Table
from baserow.core.mixins import CreatedAndUpdatedOnMixin

User = get_user_model()


class RowComment(CreatedAndUpdatedOnMixin, models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    row_id = models.PositiveIntegerField()
    # TODO: Should we instead SET_NULL or just cache the Username here? What do we
    #  want to do when a user is deleted?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        ordering = ("created_on",)
        indexes = [models.Index(fields=["table", "row_id", "created_on"])]
