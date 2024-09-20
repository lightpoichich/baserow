import json
import uuid
from os.path import join
from typing import Optional
from zipfile import ZIP_DEFLATED, ZipFile

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from opentelemetry import trace

from baserow.core.registries import ImportExportConfig, application_type_registry
from baserow.core.telemetry.utils import baserow_trace_methods
from baserow.core.utils import ChildProgressBuilder

tracer = trace.get_tracer(__name__)


class ImportExportHandler(metaclass=baserow_trace_methods(tracer)):
    def export_application(
        self, app, import_export_config, files_zip, storage, progress
    ):
        application = app.specific
        application_type = application_type_registry.get_by_model(application)

        with application_type.export_safe_transaction_context(application):
            exported_application = application_type.export_serialized(
                application, import_export_config, files_zip, storage
            )
        progress.increment()
        return exported_application

    def export_multiple_applications(
        self, applications, import_export_config, files_zip, storage, progress
    ):
        exported_applications = []

        for app in applications:
            exported_application = self.export_application(
                app, import_export_config, files_zip, storage, progress
            )
            exported_applications.append(exported_application)
        return exported_applications

    def export_json_data(self, file_name, exported_applications, files_zip, storage):
        temp_json_file_name = f"temp_{file_name}"
        temp_json_file_path = storage.save(temp_json_file_name, ContentFile(""))

        with storage.open(temp_json_file_path, "w") as temp_json_file:
            json.dump(exported_applications, temp_json_file, indent=None)

        with storage.open(temp_json_file_path, "rb") as temp_json_file:
            files_zip.write(temp_json_file.name, file_name)
        storage.delete(temp_json_file_path)

    def get_export_path(self, file_name):
        return join(settings.EXPORT_FILES_DIRECTORY, file_name)

    def export_workspace_applications(
        self,
        workspace,
        import_export_config: ImportExportConfig,
        applications=None,
        storage=None,
        progress_builder: Optional[ChildProgressBuilder] = None,
    ):
        """
        Create zip file with exported applications. If application_ids is provided, only
        those applications will be exported.

        :param workspace: The workspace of which the applications must be exported.
        :type workspace: Workspace
        :param applications: A list of Application instances that must be exported. If
             not provided, all applications will be exported.
        :param storage: The storage where the files can be loaded from.
        :type storage: Storage or None
        :param import_export_config: provides configuration options for the
            import/export process to customize how it works.
        :param progress_builder:
        :return: file name of the zip file with exported data
        :rtype: str
        """

        # Note: this needs to be imported here to avoid circular imports
        from baserow.contrib.database.export.handler import (
            _create_storage_dir_if_missing_and_open,
        )

        storage = storage or default_storage
        applications = applications or []

        progress = ChildProgressBuilder.build(progress_builder, child_total=100)
        export_app_progress = progress.create_child(80, len(applications) or 1)

        zip_file_name = f"workspace_{workspace.id}_{uuid.uuid4()}.zip"
        json_file_name = f"data/workspace_export.json"

        export_path = self.get_export_path(zip_file_name)

        with _create_storage_dir_if_missing_and_open(
            export_path, storage
        ) as files_buffer:
            with ZipFile(files_buffer, "a", ZIP_DEFLATED, False) as files_zip:
                exported_applications = self.export_multiple_applications(
                    applications,
                    import_export_config,
                    files_zip,
                    storage,
                    export_app_progress,
                )
                self.export_json_data(
                    json_file_name, exported_applications, files_zip, storage
                )
                progress.increment(by=20)
        return zip_file_name
