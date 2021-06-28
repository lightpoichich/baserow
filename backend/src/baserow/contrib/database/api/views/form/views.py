from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.decorators import map_exceptions
from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.api.schemas import get_error_schema
from baserow.contrib.database.api.views.errors import ERROR_VIEW_DOES_NOT_EXIST
from baserow.contrib.database.views.exceptions import ViewDoesNotExist
from baserow.contrib.database.views.handler import ViewHandler
from baserow.contrib.database.views.models import FormView
from baserow.contrib.database.views.registries import view_type_registry
from baserow.core.exceptions import UserNotInGroup

form_view_serializer_class = view_type_registry.get("form").get_serializer_class()


class RotateFormViewSlugView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                required=False,
                description="Rotates the slug of the provided value.",
            )
        ],
        tags=["Database table form view"],
        operation_id="rotate_database_table_form_view_slug",
        description=(
            "Rotates the unique slug of the form view by replacing it with a new value."
        ),
        responses={
            200: form_view_serializer_class(many=True),
            400: get_error_schema(["ERROR_USER_NOT_IN_GROUP"]),
            404: get_error_schema(["ERROR_VIEW_DOES_NOT_EXIST"]),
        },
    )
    @map_exceptions(
        {
            UserNotInGroup: ERROR_USER_NOT_IN_GROUP,
            ViewDoesNotExist: ERROR_VIEW_DOES_NOT_EXIST,
        }
    )
    def post(self, request, view_id):
        """Rotates the form slug."""

        handler = ViewHandler()
        form = ViewHandler().get_view(view_id, FormView)
        form = handler.rotate_form_view_slug(request.user, form)
        return Response(form_view_serializer_class(form).data)
