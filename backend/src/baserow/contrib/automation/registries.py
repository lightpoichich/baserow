from typing import TYPE_CHECKING, TypeVar

from django.db import transaction
from django.db.models import Prefetch

from baserow.core.registries import connection_type_registry, user_action_type_registry
from baserow.core.registry import (
    Instance,
    ModelInstanceMixin,
    ModelRegistryMixin,
    Registry,
    inherit_registry,
)

from .exceptions import TriggerTypeAlreadyRegistered, TriggerTypeDoesNotExist
from .models import AutomationRun
from .tasks import run_next_action

if TYPE_CHECKING:
    from .models import Trigger

TriggerTypeSubClassInstance = TypeVar("TriggerTypeSubClassInstance", bound="Trigger")


class TriggerType(
    ModelInstanceMixin["Trigger"],
    Instance,
):
    """
    @TODO docs
    """

    connection_type = None

    def enhance_find_triggers_queryset(self, queryset, **kwargs):
        return queryset

    def get_find_trigger_queryset(self, **kwargs):
        """
        Responsible for figuring out which triggers stored in the database match the
        signal/task kwargs.
        """

        connection_type = connection_type_registry.get(self.connection_type)
        connection_type_model_class = connection_type.model_class
        connection_queryset = connection_type.enhance_queryset(
            connection_type_model_class.objects.all()
        )

        queryset = self.model_class.objects.select_related(
            "automation"
        ).prefetch_related(Prefetch("connection", queryset=connection_queryset))

        return self.enhance_find_triggers_queryset(queryset, **kwargs)

    def prepare_runs(self, triggers, **kwargs):
        return [
            AutomationRun(
                automation=trigger.automation,
                trigger_payload=self.get_payload(trigger, **kwargs),
            )
            for trigger in triggers
        ]

    def get_payload(self, trigger, **kwargs):
        raise NotImplementedError

    def get_test_kwargs(self, trigger):
        raise NotImplementedError

    def dispatch(self, **kwargs):
        triggers = self.get_find_trigger_queryset(**kwargs)
        runs = self.prepare_runs(triggers, **kwargs)

        for run in runs:
            if run.has_failed:
                run.trigger_payload = None

        runs = AutomationRun.objects.bulk_create(runs)

        for run in runs:
            if not run.has_completed:
                transaction.on_commit(lambda: run_next_action.delay(run_id=run.id))


class TriggerTypeRegistry(
    ModelRegistryMixin[TriggerTypeSubClassInstance, TriggerType],
    Registry[TriggerType],
):
    """
    @TODO docs
    """

    name = "automation_trigger"
    does_not_exist_exception_class = TriggerTypeDoesNotExist
    already_registered_exception_class = TriggerTypeAlreadyRegistered


trigger_registry = TriggerTypeRegistry()
automation_action_registry = inherit_registry(user_action_type_registry)
