from django.conf.urls import url

from baserow_premium.api.admin.groups.views import GroupsAdminView


app_name = "baserow_premium.api.admin.groups"

urlpatterns = [
    url(r"^$", GroupsAdminView.as_view(), name="list"),
]
