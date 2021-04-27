from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.decorators import validate_body, map_exceptions
from baserow.api.pagination import PageNumberPagination
from baserow.api.schemas import get_error_schema
from baserow_premium.api.user_admin.errors import ERROR_ADMIN_ONLY_OPERATION
from baserow_premium.api.user_admin.serializers import AdminUserSerializer
from baserow_premium.user_admin.exceptions import AdminOnlyOperationException
from baserow_premium.user_admin.handler import UserAdminHandler


class UsersAdminView(APIView):
    @extend_schema(
        tags=["Premium", "Admin"],
        operation_id="admin_list_users",
        description="Returns all baserow users with detailed information on each user.",
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="If provided only users with a username that matches the "
                "search query will be returned.",
            ),
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                description="Defines which page of users should be returned.",
            ),
            OpenApiParameter(
                name="size",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                description="Defines how many users should be returned per page.",
            ),
        ],
        responses={
            200: AdminUserSerializer(many=True),
            400: get_error_schema(
                [
                    "ERROR_PAGE_SIZE_LIMIT",
                    "ERROR_INVALID_PAGE",
                ]
            ),
            401: get_error_schema(["ERROR_ADMIN_ONLY_OPERATION"]),
        },
    )
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def get(self, request):
        """
        Lists all the users of a user, optionally filtering on username by the
        'search' get parameter.
        """

        search = request.GET.get("search")

        handler = UserAdminHandler()
        users = handler.get_users(request.user)
        if search:
            users = users.filter(username__icontains=search)
        paginator = PageNumberPagination(limit_page_size=100)
        page = paginator.paginate_queryset(users, request, self)
        serializer = AdminUserSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class UserAdminView(APIView):
    @extend_schema(
        tags=["Premium", "Admin"],
        request=AdminUserSerializer,
        operation_id="admin_edit_user",
        description="Updates specified user attributes and returns the updated user.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                description="The id of the user to edit",
            ),
        ],
        responses={
            200: AdminUserSerializer(many=True),
            400: get_error_schema(["ERROR_REQUEST_BODY_VALIDATION"]),
            401: get_error_schema(["ERROR_ADMIN_ONLY_OPERATION"]),
        },
    )
    @validate_body(AdminUserSerializer, partial=True)
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def patch(self, request, user_id, data):
        """
        Updates the specified user with the supplied attributes.
        """

        handler = UserAdminHandler()
        user = handler.update_user(request.user, user_id, data)

        return Response(AdminUserSerializer(user).data)

    @extend_schema(
        tags=["Admin", "Premium"],
        operation_id="admin_delete_user",
        description="Deletes the specified user.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                description="The id of the user to delete",
            ),
        ],
        responses={
            200: None,
            401: get_error_schema(["ERROR_ADMIN_ONLY_OPERATION"]),
        },
    )
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def delete(self, request, user_id):
        """
        Deletes the specified user.
        """

        handler = UserAdminHandler()
        handler.delete_user(request.user, user_id)

        return Response()
