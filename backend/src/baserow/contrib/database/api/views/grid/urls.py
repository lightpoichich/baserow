from django.conf.urls import url

from .views import GridViewView, GridViewFieldOrdersView


app_name = 'baserow.contrib.database.api.views.grid'

urlpatterns = [
    url(r'(?P<view_id>[0-9]+)/$', GridViewView.as_view(), name='list'),
    url(
        r'(?P<view_id>[0-9]+)/field-orders/$',
        GridViewFieldOrdersView.as_view(),
        name='field_orders'
    ),
]
