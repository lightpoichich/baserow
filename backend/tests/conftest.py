from __future__ import print_function

import sys
import threading
from contextlib import contextmanager
from functools import partial

from django.core.management import call_command
from django.db import connections
from django.test.testcases import TransactionTestCase

import pytest
from loguru import logger

# noinspection PyUnresolvedReferences
from baserow.test_utils.pytest_conftest import *  # noqa: F403, F401


def _fixture_teardown(self):
    """
    This is a custom implementation of `TransactionTestCase._fixture_teardown`
    from Django (https://github.com/django/django/blob/main/django/test/testcases.py)
    that flushes test database after test runs with allow_cascade=True.

    This is needed as our custom Baserow tables won't be in the list of tables
    to truncate, and hence may create problems when rows are
    referencing other tables.
    """

    # Allow TRUNCATE ... CASCADE and don't emit the post_migrate signal
    # when flushing only a subset of the apps
    for db_name in self._databases_names(include_mirrors=False):
        # Flush the database
        inhibit_post_migrate = (
            self.available_apps is not None
            or (  # Inhibit the post_migrate signal when using serialized
                # rollback to avoid trying to recreate the serialized data.
                self.serialized_rollback
                and hasattr(connections[db_name], "_test_serialized_contents")
            )
        )
        call_command(
            "flush",
            verbosity=0,
            interactive=False,
            database=db_name,
            reset_sequences=False,
            allow_cascade=True,  # CHANGED FROM DJANGO
            inhibit_post_migrate=inhibit_post_migrate,
        )


TransactionTestCase._fixture_teardown = _fixture_teardown


@pytest.fixture()
def test_thread():
    """
    Run a side thread with an arbitrary function.

    This fixture allows to run a helper thread with an arbitrary function
    to test concurrent flows, i.e. in-Celery-task state changes.

    This fixture will increase min thread switching granularity for the test to
    to 0.00001s.

    It's advised to use threading primitives to communicate with the helper thread.

    A callable will be wrapped to log any error ocurred during the execution.

    A Thread object yielded from this fixture has .thread_stopped Event attached to
    simplify synchronization with the test code. This event is set when a
    callable finished it's work.

    >>> def test_x(test_thread):
        evt_start = threading.Event()
        evt_end = threading.Event()
        evt_can_end = threading.Event()

        def callable(*args, **kwargs):
            evt_start.set()
            assert evt_can_end(timeout=0.01)
            evt_end.set()

        with test_thread(callable, foo='bar') as t:
             # pick a moment to start
             t.start()
             evt_can_end.set()

             # wait for the callable to finish
             assert t.thread_stopped.wait(0.1)

        assert evt_start.is_set()
        assert evt_end.is_set()

    :return:
    """

    thread_stopped = threading.Event()

    def wrapper(c, *args, **kwargs):
        try:
            logger.info(f"running callable {c} with args {args} {kwargs}")
            return c(*args, **kwargs)
        except Exception as err:
            logger.error(f"error when running {c}: {err}", exc_info=True)
            raise
        finally:
            thread_stopped.set()

    @contextmanager
    def run_callable(callable, *args, **kwargs):
        t = threading.Thread(target=partial(wrapper, callable, *args, **kwargs))
        t.thread_stopped = thread_stopped
        switch_interval = 0.00001
        orig_switch_interval = sys.getswitchinterval()
        try:
            sys.setswitchinterval(switch_interval)
            yield t
        finally:
            while t.is_alive():
                t.join(0.01)
            sys.setswitchinterval(orig_switch_interval)

    yield run_callable
