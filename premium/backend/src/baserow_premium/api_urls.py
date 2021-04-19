from django.conf.urls import url

from baserow_premium.views import UserAdminView

app_name = "baserow_premium"

urlpatterns = [
    url(r"^users/$", UserAdminView.as_view(), name="users"),
]
