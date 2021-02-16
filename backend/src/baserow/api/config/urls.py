from django.conf.urls import url

from .views import ConfigView, ConfigUpdateView


app_name = 'baserow.api.config'

urlpatterns = [
    url(r'^update/$', ConfigUpdateView.as_view(), name='update'),
    url(r'^$', ConfigView.as_view(), name='get'),
]
