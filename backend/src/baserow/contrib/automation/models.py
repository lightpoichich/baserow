from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from baserow.core.mixins import PolymorphicContentTypeMixin
from baserow.core.models import Application, Connection


def get_default_trigger_content_type():
    return ContentType.objects.get_for_model(Trigger)


def get_default_action_content_type():
    return ContentType.objects.get_for_model(UserAction)


class Trigger(PolymorphicContentTypeMixin, models.Model):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="automation_triggers",
        on_delete=models.SET(get_default_trigger_content_type),
    )
    connection = models.ForeignKey(
        Connection,
        verbose_name="connection",
        related_name="automation_triggers",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class Automation(Application):
    trigger = models.OneToOneField(
        Trigger,
        null=True,
        default=None,
        related_name="automation",
        on_delete=models.SET_NULL,
    )


class UserAction(PolymorphicContentTypeMixin, models.Model):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="automation_user_actions",
        on_delete=models.SET(get_default_trigger_content_type),
    )
    connection = models.ForeignKey(
        Connection,
        verbose_name="connection",
        related_name="automation_user_actions",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    automation = models.ForeignKey(
        Automation,
        verbose_name="content type",
        related_name="user_actions",
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="parents",
        related_name="children",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class AutomationRun(models.Model):
    automation = models.ForeignKey(
        Automation,
        related_name="runs",
        on_delete=models.CASCADE,
    )
    failed_at = models.DateTimeField(null=True)
    failed_error = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True)
    trigger_payload = models.JSONField(null=True)

    @property
    def has_failed(self):
        return self.failed_at is not None

    @property
    def has_completed(self):
        return self.has_failed or self.completed_at is not None

    def fail(self, reason):
        self.failed_at = timezone.now()
        self.failed_error = reason

    def complete(self):
        self.completed_at = timezone.now()


class AutomationRunUserAction(models.Model):
    automation_run = models.ForeignKey(
        AutomationRun,
        verbose_name="automation run",
        related_name="user_actions",
        on_delete=models.CASCADE,
    )
    action = models.ForeignKey(
        UserAction,
        verbose_name="user action",
        related_name="automation_run_user_actions",
        on_delete=models.CASCADE
    )
    action_payload = models.JSONField(null=True)
