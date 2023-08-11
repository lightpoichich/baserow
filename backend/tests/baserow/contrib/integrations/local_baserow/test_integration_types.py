import pytest

from baserow.contrib.builder.exceptions import InvalidIntegrationAuthorizedUser
from baserow.core.integrations.registries import integration_type_registry
from baserow.core.integrations.service import IntegrationService


@pytest.mark.django_db
def test_create_local_baserow_integration_with_user(data_fixture):
    user = data_fixture.create_user()
    application = data_fixture.create_builder_application(user=user)

    integration_type = integration_type_registry.get("local_baserow")

    integration = IntegrationService().create_integration(
        user, integration_type, application=application, authorized_user=user
    )

    assert integration.authorized_user.id == user.id


@pytest.mark.django_db
def test_validate_local_baserow_integration_with_authorized_user_not_in_workspace(
    data_fixture,
):
    user = data_fixture.create_user()
    authorized_user = data_fixture.create_user()
    application = data_fixture.create_builder_application(user=user)
    integration_type = integration_type_registry.get("local_baserow")

    with pytest.raises(InvalidIntegrationAuthorizedUser) as exc_info:
        integration_type.validate(
            application,
            integration_type.prepare_values({"authorized_user": authorized_user}, user),
        )
    assert (
        exc_info.value.args[0] == f"The user {authorized_user.pk} does not belong "
        "to the integration's workspace."
    )


@pytest.mark.django_db
def test_validate_local_baserow_integration_with_authorized_user_flagged_for_deletion(
    data_fixture,
):
    user = data_fixture.create_user()
    authorized_user = data_fixture.create_user(to_be_deleted=True)
    application = data_fixture.create_builder_application(user=authorized_user)
    integration_type = integration_type_registry.get("local_baserow")

    with pytest.raises(InvalidIntegrationAuthorizedUser) as exc_info:
        integration_type.validate(
            application,
            integration_type.prepare_values({"authorized_user": authorized_user}, user),
        )
    assert (
        exc_info.value.args[0]
        == f"The user {authorized_user.id} is flagged for deletion."
    )


@pytest.mark.django_db
def test_validate_local_baserow_integration_without_passing_authorized_user(
    data_fixture,
):
    user = data_fixture.create_user()
    application = data_fixture.create_builder_application(user=user)
    integration_type = integration_type_registry.get("local_baserow")
    IntegrationService().create_integration(
        user, integration_type, application=application, authorized_user=user
    )

    try:
        integration_type.validate(
            application,
            integration_type.prepare_values({}, user),
        )
    except (AttributeError, InvalidIntegrationAuthorizedUser):
        pytest.fail(
            "Validating a local_baserow integration type "
            "without an authorized_user should be permitted."
        )
