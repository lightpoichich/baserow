from django.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^api/', include('baserow.api.v0.urls', namespace='api')),
]
