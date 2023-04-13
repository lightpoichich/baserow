from django.db import transaction

from baserow.config.celery import app
from baserow.core.registries import connection_type_registry
from baserow.contrib.automation.registries import user_action_type_registry

from .models import AutomationRun, AutomationRunUserAction


@app.task(bind=True, queue="export")
def dispatch_trigger(self, trigger_type_name, **kwargs: dict):
    from baserow.contrib.automation.registries import trigger_registry

    trigger_registry.get(trigger_type_name).dispatch(**kwargs)


@app.task(bind=True, queue="export")
def run_next_action(self, run_id):
    run = AutomationRun.objects.select_related("automation").get(
        id=run_id
    )

    if run.has_completed:
        return

    run_user_actions = run.user_actions.all()

    if len(run_user_actions) == 0:
        # If none of the actions ran before, we must find the first user action
        # without a parent and run that one.
        action_to_run = run.automation.user_actions.filter(parent=None).first()
    else:
        # Find the child of the last action and run that one.
        last_action_id = run_user_actions[len(run_user_actions) - 1].action_id
        action_to_run = run.automation.user_actions.filter(
            parent_id=last_action_id
        ).first()

    if action_to_run is None:
        run.complete()
        run.save()
        return

    action_to_run = action_to_run.specific
    user_action_type = user_action_type_registry.get_by_model(action_to_run)

    # @TODO make this nicer.
    if user_action_type.connection_type is not None:
        connection_type = connection_type_registry.get(user_action_type.connection_type)
        connection_type_model_class = connection_type.model_class
        connection_queryset = connection_type.enhance_queryset(
            connection_type_model_class.objects.filter(id=action_to_run.connection_id)
        ).get()
        action_to_run.connection = connection_queryset

    try:
        result = user_action_type.dispatch(action_to_run)
    except Exception:
        run.fail("@TODO")
        run.save()
        raise Exception("Something went wrong while dispatching user action.")

    AutomationRunUserAction.objects.create(
        automation_run=run,
        action=action_to_run,
        action_payload=result
    )

    transaction.on_commit(lambda: run_next_action.delay(run_id))
