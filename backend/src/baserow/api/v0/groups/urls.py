from django.conf.urls import url

from .views import GroupsView


app_name = 'baserow.api.v0.group'

urlpatterns = [
    url(r'^$', GroupsView.as_view(), name='list')
]
