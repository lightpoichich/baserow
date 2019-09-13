import pytest

from baserow.core.applications import Application, ApplicationRegistry
from baserow.core.exceptions import ApplicationAlreadyRegistered


class TemporaryApplication1(Application):
    type = 'temporary_1'
    instance_model = object


class TemporaryApplication2(Application):
    type = 'temporary_2'
    instance_model = object


def test_application_registry_register():
    temporary_1 = TemporaryApplication1()
    temporary_2 = TemporaryApplication2()

    registry = ApplicationRegistry()
    registry.register(temporary_1)
    registry.register(temporary_2)

    with pytest.raises(ValueError):
        registry.register('NOT AN APPLICATION')

    with pytest.raises(ApplicationAlreadyRegistered):
        registry.register(temporary_1)

    assert len(registry.registry.items()) == 2
    assert registry.registry['temporary_1'] == temporary_1
    assert registry.registry['temporary_2'] == temporary_2

    registry.unregister(temporary_1)

    assert len(registry.registry.items()) == 1

    registry.unregister('temporary_2')

    assert len(registry.registry.items()) == 0

    with pytest.raises(ValueError):
        registry.unregister(000)
