from django.urls import re_path

from .views import PublicTimelineViewView, TimelineViewView

app_name = "baserow_premium.api.views.timeline"

urlpatterns = [
    re_path(r"(?P<view_id>[0-9]+)/$", TimelineViewView.as_view(), name="list"),
    re_path(
        r"(?P<slug>[-\w]+)/public/rows/$",
        PublicTimelineViewView.as_view(),
        name="public_rows",
    ),
]
