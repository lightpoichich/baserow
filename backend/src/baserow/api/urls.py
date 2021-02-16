from django.urls import path, include

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView

from baserow.core.registries import plugin_registry, application_type_registry

from .config import urls as config_urls
from .user import urls as user_urls
from .user_files import urls as user_files_urls
from .groups import urls as group_urls
from .applications import urls as application_urls


app_name = 'baserow.api'

urlpatterns = [
    path('schema.json', SpectacularJSONAPIView.as_view(), name='json_schema'),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='api:json_schema'),
        name='redoc'
    ),
    path('config/', include(config_urls, namespace='config')),
    path('user/', include(user_urls, namespace='user')),
    path('user-files/', include(user_files_urls, namespace='user_files')),
    path('groups/', include(group_urls, namespace='groups')),
    path('applications/', include(application_urls, namespace='applications'))
] + application_type_registry.api_urls + plugin_registry.api_urls
