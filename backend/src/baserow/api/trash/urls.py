from django.conf.urls import url

from .views import TrashContentsView, TrashStructureView, TrashItemView

app_name = "baserow.api.trash"

urlpatterns = [
    url(r"^$", TrashStructureView.as_view(), name="list"),
    url(
        r"^group/(?P<group_id>[0-9]+)/$",
        TrashContentsView.as_view(),
        name="contents",
    ),
    # TODO Trash - Enforce this regex on registry types also
    url(
        r"^item/(?P<trash_item_type>[A-Za-z0-9]+)/(?P<trash_item_id>[0-9]+)/$",
        TrashItemView.as_view(),
        name="restore",
    ),
]
