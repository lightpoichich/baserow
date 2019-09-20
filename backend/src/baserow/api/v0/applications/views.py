from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from baserow.api.v0.decorators import validate_body
from baserow.core.models import GroupUser, Application
from baserow.core.handler import CoreHandler

from .serializers import ApplicationSerializer, ApplicationCreateSerializer


class ApplicationsView(APIView):
    permission_classes = (IsAuthenticated,)
    core_handler = CoreHandler()

    def load_group(self, request, group_id):
        return get_object_or_404(
            GroupUser.objects.select_related('group'),
            group_id=group_id,
            user=request.user
        )

    def get(self, request, group_id):
        """
        Responds with a list of applications that belong to the group if the user has
        access to that group.
        """

        group_user = self.load_group(request, group_id)
        applications = Application.objects.filter(
            group=group_user.group
        ).select_related('content_type')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @transaction.atomic
    @validate_body(ApplicationCreateSerializer)
    def post(self, request, data, group_id):
        """Creates a new group for a user."""
        group_user = self.load_group(request, group_id)
        application = self.core_handler.create_application(
            request.user, group_user.group, data['type'], name=data['name'])

        return Response(ApplicationSerializer(application).data)
