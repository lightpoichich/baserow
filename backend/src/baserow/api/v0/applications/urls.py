from django.conf.urls import url

from .views import ApplicationsView


app_name = 'baserow.api.v0.group'

urlpatterns = [
    url(r'(?P<group_id>[0-9]+)/$', ApplicationsView.as_view(), name='list')
]
