from django.conf.urls import url

from .views import TemplatesView


app_name = 'baserow.api.templates'


urlpatterns = [
    url(r'$', TemplatesView.as_view(), name='list'),
]
