from typing import Any, Dict, List

from django.contrib.auth.models import AbstractUser

from rest_framework import serializers

from baserow.api.applications.errors import ERROR_APPLICATION_DOES_NOT_EXIST
from baserow.api.applications.serializers import (
    InstallTemplateJobApplicationsSerializer,
    PolymorphicApplicationResponseSerializer,
)
from baserow.api.errors import (
    ERROR_GROUP_DOES_NOT_EXIST,
    ERROR_MAX_LOCKS_PER_TRANSACTION_EXCEEDED,
    ERROR_USER_NOT_IN_GROUP,
)
from baserow.api.templates.errors import (
    ERROR_TEMPLATE_DOES_NOT_EXIST,
    ERROR_TEMPLATE_FILE_DOES_NOT_EXIST,
)
from baserow.api.templates.serializers import TemplateSerializer
from baserow.api.workspaces.serializers import WorkspaceSerializer
from baserow.contrib.database.api.export.serializers import (
    ExportedFileURLSerializerMixin,
)
from baserow.core.action.registries import action_type_registry
from baserow.core.actions import (
    DuplicateApplicationActionType,
    InstallTemplateActionType,
    ExportApplicationsActionType,
)
from baserow.core.db import read_repeatable_multiple_applications_atomic_transaction
from baserow.core.exceptions import (
    ApplicationDoesNotExist,
    DuplicateApplicationMaxLocksExceededException,
    TemplateDoesNotExist,
    TemplateFileDoesNotExist,
    UserNotInWorkspace,
    WorkspaceDoesNotExist,
)
from baserow.core.handler import CoreHandler
from baserow.core.jobs.registries import JobType
from baserow.core.models import (
    Application,
    DuplicateApplicationJob,
    ExportApplicationsJob,
    InstallTemplateJob,
)
from baserow.core.operations import CreateApplicationsWorkspaceOperationType
from baserow.core.registries import application_type_registry
from baserow.core.utils import Progress


class DuplicateApplicationJobType(JobType):
    type = "duplicate_application"
    model_class = DuplicateApplicationJob
    max_count = 1

    api_exceptions_map = {
        UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
        WorkspaceDoesNotExist: ERROR_GROUP_DOES_NOT_EXIST,
        DuplicateApplicationMaxLocksExceededException: ERROR_MAX_LOCKS_PER_TRANSACTION_EXCEEDED,
    }

    job_exceptions_map = {
        DuplicateApplicationMaxLocksExceededException: DuplicateApplicationMaxLocksExceededException.message
    }

    request_serializer_field_names = ["application_id"]

    request_serializer_field_overrides = {
        "application_id": serializers.IntegerField(
            help_text="The application ID to duplicate.",
        ),
    }

    serializer_field_names = ["original_application", "duplicated_application"]
    serializer_field_overrides = {
        "original_application": PolymorphicApplicationResponseSerializer(
            read_only=True
        ),
        "duplicated_application": PolymorphicApplicationResponseSerializer(
            read_only=True
        ),
    }

    def transaction_atomic_context(self, job: "DuplicateApplicationJob"):
        application = (
            CoreHandler()
            .get_user_application(job.user, job.original_application_id)
            .specific
        )
        application_type = application_type_registry.get_by_model(
            application.specific_class
        )
        return application_type.export_safe_transaction_context(application)

    def prepare_values(
        self, values: Dict[str, Any], user: AbstractUser
    ) -> Dict[str, Any]:
        application = (
            CoreHandler().get_user_application(user, values["application_id"]).specific
        )

        return {
            "original_application": application,
        }

    def run(self, job: DuplicateApplicationJob, progress: Progress) -> Application:
        new_application_clone = action_type_registry.get_by_type(
            DuplicateApplicationActionType
        ).do(
            job.user,
            job.original_application,
            progress_builder=progress.create_child_builder(
                represents_progress=progress.total
            ),
        )

        # update the job with the new duplicated application
        job.duplicated_application = new_application_clone
        job.save(update_fields=("duplicated_application",))

        return new_application_clone


class InstallTemplateJobType(JobType):
    type = "install_template"
    model_class = InstallTemplateJob
    max_count = 1

    api_exceptions_map = {
        UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
        WorkspaceDoesNotExist: ERROR_GROUP_DOES_NOT_EXIST,
        TemplateDoesNotExist: ERROR_TEMPLATE_DOES_NOT_EXIST,
        TemplateFileDoesNotExist: ERROR_TEMPLATE_FILE_DOES_NOT_EXIST,
    }

    request_serializer_field_names = [
        "workspace_id",
        "database_id",
        "airtable_share_url",
    ]

    request_serializer_field_overrides = {
        "workspace_id": serializers.IntegerField(
            required=False,
            help_text="The ID of the workspace where the template will be installed.",
        ),
        "template_id": serializers.IntegerField(
            help_text="The template ID that will be installed.",
        ),
    }

    serializer_field_names = [
        "workspace",
        "template",
        "installed_applications",
    ]
    serializer_field_overrides = {
        "workspace": WorkspaceSerializer(read_only=True),
        "template": TemplateSerializer(read_only=True),
        "installed_applications": InstallTemplateJobApplicationsSerializer(
            read_only=True
        ),
    }

    def prepare_values(
        self, values: Dict[str, Any], user: AbstractUser
    ) -> Dict[str, Any]:
        handler = CoreHandler()
        workspace = handler.get_workspace(values["workspace_id"])
        CoreHandler().check_permissions(
            user,
            CreateApplicationsWorkspaceOperationType.type,
            workspace=workspace,
            context=workspace,
        )

        # ensure everything is ok for the installation, otherwise
        # raise an exception immediately without submitting the job
        template = handler.get_template(values["template_id"])
        handler.get_valid_template_path_or_raise(template)

        return {
            "workspace": workspace,
            "template": template,
        }

    def run(self, job: InstallTemplateJob, progress: Progress) -> List[Application]:
        progress_builder = progress.create_child_builder(
            represents_progress=progress.total
        )

        installed_applications = action_type_registry.get_by_type(
            InstallTemplateActionType
        ).do(job.user, job.workspace, job.template, progress_builder=progress_builder)

        job.installed_applications = [app.id for app in installed_applications]
        job.save(update_fields=("installed_applications",))

        return installed_applications


class ExportApplicationsJobType(JobType):
    type = "export_applications"
    model_class = ExportApplicationsJob
    max_count = 1

    api_exceptions_map = {
        UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
        WorkspaceDoesNotExist: ERROR_GROUP_DOES_NOT_EXIST,
        ApplicationDoesNotExist: ERROR_APPLICATION_DOES_NOT_EXIST,
    }

    job_exceptions_map = {
        # TODO: Add the exception error messages
    }

    request_serializer_field_names = ["workspace_id", "application_ids"]
    # TODO: It doesn't accept empty value, empty list
    request_serializer_field_overrides = {
        "application_ids": serializers.ListField(
            allow_null=True,
            allow_empty=True,
            required=False,
            child=serializers.IntegerField(),
            help_text=(
                "The application IDs to export. If not provided, all the applications for "
                "the workspace will be exported."
            ),
        ),
        'structure_only': serializers.BooleanField(
            required=False,
            default=False,
            help_text=(
                "If True, only the structure of the applications will be exported. "
                "If False, the data will be included as well."
            )
        ),
    }

    serializer_mixins = [ExportedFileURLSerializerMixin]
    serializer_field_names = ["exported_file_name", "url"]

    def transaction_atomic_context(self, job: "DuplicateApplicationJob"):
        return read_repeatable_multiple_applications_atomic_transaction(job.application_ids)

    def prepare_values(
        self, values: Dict[str, Any], user: AbstractUser
    ) -> Dict[str, Any]:
        # validate that the workspace exists, the user have access to it
        # if provided validate the all the applications ids exist and the user has access to them
        # if not provided, get all the applications the user has access to and return the ids


        workspace_id = values.get("workspace_id")
        application_ids = values.get("application_ids")

        queryset = Application.objects.filter(workspace_id=workspace_id)
        if application_ids:
            queryset = queryset.filter(id__in=application_ids)

        applications = queryset.all()
        # if len(applications) == len(applications_ids) otherwise raise a not found exception
        # CoreHandler().check_permissions(
        #     user,
        #     ReadApplicationsWorkspaceOperationType.type,
        #     workspace=workspace,
        #     context=workspace,
        # )
        # # ensure all the applications are accessible by the user

        return {
            "workspace_id": workspace_id,
            "application_ids": ",".join(application_ids) if application_ids else "",
        }

    def run(self, job: ExportApplicationsJob, progress: Progress) -> str:
        # redo the same checks and fail if something changed in the meantime

        application_ids = None
        if job.application_ids:
            application_ids = [int(app_id) for app_id in job.application_ids.split(",")]

        exported_file_name = action_type_registry.get_by_type(
            ExportApplicationsActionType
        ).do(
            job.user,
            job.workpace_id,
            application_ids,
            progress_builder=progress.create_child_builder(
                represents_progress=progress.total
            ),
        )

        # update the job with the new duplicated application
        job.exported_file_name = exported_file_name
        job.save(update_fields=("exported_file_name",))

        return exported_file_name
