from django.urls import re_path

from .views import ExportJobView, ExportTableView, AsyncExportApplicationsView

app_name = "baserow.contrib.database.api.export"

urlpatterns = [
    re_path(
        r"table/(?P<table_id>[0-9]+)/$",
        ExportTableView.as_view(),
        name="export_table",
    ),
    re_path(
        r"workspace/(?P<workspace_id>[0-9]+)/async/$",
        AsyncExportApplicationsView.as_view(),
        name="export_workspace_async",
    ),
    re_path(r"(?P<job_id>[0-9]+)/$", ExportJobView.as_view(), name="get"),
]
