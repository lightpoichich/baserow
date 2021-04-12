from django.conf.urls import url

from .views import RowsView, RowView


app_name = "baserow.contrib.database.api.rows"

urlpatterns = [
    url(r"table/(?P<table_id>[0-9]+)/$", RowsView.as_view(), name="list"),
    url(
        r"table/(?P<table_id>[0-9]+)/(?P<row_id>[0-9]+)/$",
        RowView.as_view(),
        name="item",
    ),
]
