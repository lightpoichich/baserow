from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model

from rest_framework import serializers

from baserow.contrib.builder.exceptions import InvalidIntegrationAuthorizedUser
from baserow.contrib.integrations.local_baserow.models import LocalBaserowIntegration
from baserow.core.integrations.registries import IntegrationType
from baserow.core.integrations.types import IntegrationDict
from baserow.core.models import Application

User = get_user_model()


class LocalBaserowIntegrationType(IntegrationType):
    type = "local_baserow"
    model_class = LocalBaserowIntegration

    class SerializedDict(IntegrationDict):
        authorized_user_username: str

    serializer_field_names = ["authorized_user"]
    allowed_fields = ["authorized_user"]

    serializer_field_overrides = {
        "authorized_user": serializers.IntegerField(
            source="authorized_user_id", help_text="The authorized user's primary key."
        ),
    }

    request_serializer_field_names = []
    request_serializer_field_overrides = {}

    def validate(self, application: "Application", prepared_values: Dict[str, Any]):
        """
        Performs some extra validation on the `LocalBaserowIntegration` authorized
        user to ensure they're part of the workspace, and not flagged for deletion.
        """

        workspace = application.workspace
        authorized_user: Optional[User] = prepared_values.get("authorized_user", None)

        if authorized_user:
            try:
                workspace.users.select_related("profile").get(id=authorized_user.id)
            except workspace.users.model.DoesNotExist:
                raise InvalidIntegrationAuthorizedUser(
                    f"The user {authorized_user.pk} does not belong "
                    "to the integration's workspace."
                )

            if authorized_user.profile.to_be_deleted:  # type: ignore
                raise InvalidIntegrationAuthorizedUser(
                    f"The user {authorized_user.pk} is flagged for deletion."
                )

    def get_property_for_serialization(
        self, integration: LocalBaserowIntegration, prop_name: str
    ):
        """
        Replace the authorized user property with its username. Better when loading the
        data later.
        """

        if prop_name == "authorized_user_username":
            if integration.authorized_user:
                return integration.authorized_user.username
            return None

        return super().get_property_for_serialization(integration, prop_name)

    def import_serialized(
        self,
        application: Application,
        serialized_values: Dict[str, Any],
        id_mapping: Dict,
        cache=None,
    ) -> LocalBaserowIntegration:
        """
        Imports a serialized integration. Handles the user part with a cache for
        better performances.
        """

        if cache is None:
            cache = {}

        if "workspace_users" not in cache:
            # In order to prevent a lot of lookup queries in the through table, we want
            # to fetch all the users and add it to a temporary in memory cache
            # containing a mapping of user per email
            cache["workspace_users"] = {
                user.username: user
                for user in User.objects.filter(
                    workspaceuser__workspace_id=id_mapping["import_workspace_id"]
                )
            }

        username = serialized_values.pop("authorized_user_username", None)

        if username:
            serialized_values["authorized_user"] = cache["workspace_users"].get(
                username, None
            )

        return super().import_serialized(
            application, serialized_values, id_mapping, cache
        )

    def enhance_queryset(self, queryset):
        return queryset.select_related("authorized_user")
