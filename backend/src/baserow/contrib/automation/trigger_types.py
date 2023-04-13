from django.core.exceptions import ImproperlyConfigured
from django.core.signals import Signal
from django.db import transaction

from .registries import TriggerType
from .tasks import dispatch_trigger


class SignalViaTaskTriggerType(TriggerType):
    """
    The purpose of this abstract trigger type is to listener when a signal is
    triggered, immediately start task when the transactions and then figure out which
    triggers must be called.
    """

    signal = None

    def __init__(self):
        if not isinstance(self.signal, Signal):
            raise ImproperlyConfigured(
                "The `signal` property must be set on webhook event types."
            )

        super().__init__()
        self.signal.connect(self.signal_listener)

    def signal_listener(self, *args, **kwargs):
        """
        Run async task when the transaction commits, so that checking if there are
        any triggers doesn't hold back the request.
        """

        kwargs = self.prepare_signal_kwargs_for_task(**kwargs)
        transaction.on_commit(
            lambda: dispatch_trigger(self.type, **kwargs)
        )

    def prepare_signal_kwargs_for_task(self, **kwargs):
        """
        Responsible for converting the signal kwargs to JSON serializable kwargs for
        the celery task.
        """

        raise NotImplementedError
