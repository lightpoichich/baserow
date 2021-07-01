from django.conf.urls import url

from .views import RotateFormViewSlugView, SubmitFormViewView


app_name = "baserow.contrib.database.api.views.form"

urlpatterns = [
    url(
        r"(?P<view_id>[0-9]+)/rotate-slug/$",
        RotateFormViewSlugView.as_view(),
        name="rotate_slug",
    ),
    url(
        r"(?P<slug>[-\w]+)/submit/$",
        SubmitFormViewView.as_view(),
        name="submit",
    ),
]
