from django.db import transaction

from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from baserow.api.decorators import validate_body
from baserow.core.handler import CoreHandler

from .serializers import ConfigSerializer


class ConfigView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['Config'],
        operation_id='get_config',
        description='Responds with all the admin configured settings.',
        responses={
            200: ConfigSerializer,
        },
        auth=[None],
    )
    def get(self, request):
        """
        Responds with all the admin configured settings.
        """

        config = CoreHandler().get_config()
        return Response(ConfigSerializer(config).data)


class ConfigUpdateView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=['Config'],
        operation_id='update_config',
        description=(
            'Updates the admin configured settings if the user has admin permissions.'
        ),
        request=ConfigSerializer,
        responses={
            200: ConfigSerializer,
        },
    )
    @validate_body(ConfigSerializer)
    @transaction.atomic
    def patch(self, request, data):
        """
        Updates the provided config settings if the user has admin permissions.
        """

        config = CoreHandler().update_config(request.user, **data)
        return Response(ConfigSerializer(config).data)
