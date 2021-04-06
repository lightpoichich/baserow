from django.conf.urls import url

from .views import TemplatesView, InstallTemplateView


app_name = 'baserow.api.templates'


urlpatterns = [
    url(
        r'(?P<group_id>[0-9]+)/(?P<template_id>[0-9]+)/$',
        InstallTemplateView.as_view(),
        name='install'
    ),
    url(r'$', TemplatesView.as_view(), name='list'),
]
