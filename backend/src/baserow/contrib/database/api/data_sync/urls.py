from django.urls import re_path

from .views import DataSyncsView, SyncDataSyncTableView

app_name = "baserow.contrib.database.api.data_sync"

urlpatterns = [
    re_path(
        r"database/(?P<database_id>[0-9]+)/$", DataSyncsView.as_view(), name="list"
    ),
    re_path(
        r"(?P<data_sync_id>[0-9]+)/sync/async/$",
        SyncDataSyncTableView.as_view(),
        name="sync_table",
    ),
]
