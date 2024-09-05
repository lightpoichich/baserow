import pytest

from baserow.core.handler import CoreHandler
from baserow.core.registries import ImportExportConfig


@pytest.mark.django_db(transaction=True)
def test_create_export_file(data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    data_fixture.create_database_application(workspace=workspace)

    cli_import_export_config = ImportExportConfig(
        include_permission_data=False, reduce_disk_space_usage=False
    )

    file_name = CoreHandler().export_workspace_applications_single_file(
        workspace=workspace, import_export_config=cli_import_export_config
    )

    assert file_name is not None
