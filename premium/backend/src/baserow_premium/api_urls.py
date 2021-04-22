from django.conf.urls import url

from baserow_premium.views import UsersAdminView, UserAdminView

app_name = "baserow_premium"

urlpatterns = [
    url(r"^user/$", UsersAdminView.as_view(), name="users"),
    url(r"^user/(?P<user_id>[0-9]+)/$", UserAdminView.as_view(), name="user_edit"),
]
