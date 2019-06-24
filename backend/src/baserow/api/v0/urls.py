from django.urls import path, include
from django.conf.urls import url

from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)


app_name = 'baserow.api.v0'
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    path('', include(router.urls)),
]
