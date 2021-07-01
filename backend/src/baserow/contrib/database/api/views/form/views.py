from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.fields import empty

from baserow.api.decorators import map_exceptions
from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.api.schemas import get_error_schema
from baserow.api.utils import validate_data
from baserow.contrib.database.api.views.errors import ERROR_VIEW_DOES_NOT_EXIST
from baserow.contrib.database.api.rows.serializers import get_row_serializer_class
from baserow.contrib.database.views.exceptions import ViewDoesNotExist
from baserow.contrib.database.views.handler import ViewHandler
from baserow.contrib.database.views.models import FormView, FormViewFieldOptions
from baserow.contrib.database.views.registries import view_type_registry
from baserow.core.exceptions import UserNotInGroup

from .errors import ERROR_FORM_DOES_NOT_EXIST
from .serializers import PublicFormViewSerializer, FormViewSubmittedSerializer

form_view_serializer_class = view_type_registry.get("form").get_serializer_class()


class RotateFormViewSlugView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                required=True,
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


class SubmitFormViewView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="slug",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="The slug related to the form.",
            )
        ],
        tags=["Database table form view"],
        operation_id="get_meta_database_table_form_view",
        description=("@TODO docs"),
        responses={
            200: PublicFormViewSerializer,
            404: get_error_schema(["ERROR_FORM_DOES_NOT_EXIST"]),
        },
    )
    @map_exceptions(
        {
            ViewDoesNotExist: ERROR_FORM_DOES_NOT_EXIST,
        }
    )
    def get(self, request, slug):
        form = ViewHandler().get_public_form_view_by_slug(request.user, slug)
        serializer = PublicFormViewSerializer(form)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="slug",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="The slug related to the form.",
            )
        ],
        tags=["Database table form view"],
        operation_id="submit_database_table_form_view",
        description=("@TODO docs"),
        responses={
            200: None,
            404: get_error_schema(["ERROR_FORM_DOES_NOT_EXIST"]),
        },
    )
    @map_exceptions(
        {
            ViewDoesNotExist: ERROR_FORM_DOES_NOT_EXIST,
        }
    )
    def post(self, request, slug):
        handler = ViewHandler()
        form = handler.get_public_form_view_by_slug(request.user, slug)
        model = form.table.get_model()

        options = FormViewFieldOptions.objects.filter(form_view=form, enabled=True)
        field_kwargs = {
            model._field_objects[option.field_id]["name"]: {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "default": empty,
            }
            for option in options
            if option.required
        }
        field_ids = [option.field_id for option in options]
        validation_serializer = get_row_serializer_class(
            model, field_ids=field_ids, field_kwargs=field_kwargs
        )
        data = validate_data(validation_serializer, request.data)

        handler.submit_form_view(form, data, model)
        return Response(FormViewSubmittedSerializer(form).data)
