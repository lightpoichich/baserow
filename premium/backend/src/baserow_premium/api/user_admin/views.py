from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.decorators import validate_body, map_exceptions
from baserow.api.pagination import PageNumberPagination
from baserow.contrib.database.api.tokens.authentications import TokenAuthentication
from baserow_premium.api.user_admin.errors import ERROR_ADMIN_ONLY_OPERATION
from baserow_premium.api.user_admin.serializers import PartialAdminUserSerializer
from baserow_premium.user_admin.exceptions import AdminOnlyOperationException
from baserow_premium.user_admin.handler import UserAdminHandler


class UsersAdminView(APIView):
    @extend_schema(
        tags=["Admin"],
        operation_id="list_users_admin",
        description="TODO",
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="If provided only users with a username that matches the "
                "search query are going to be returned.",
            ),
        ],
        responses={
            200: PartialAdminUserSerializer(many=True),
        },
    )
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def get(self, request):
        """Lists all the users of a user."""

        search = request.GET.get("search")

        handler = UserAdminHandler()
        users = handler.get_users(request.user)
        if search:
            users = users.filter(username__icontains=search)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(users, request, self)
        serializer = PartialAdminUserSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class UserAdminView(APIView):
    @extend_schema(
        tags=["Admin"],
        operation_id="edit_users_admin",
        description="TODO",
        responses={
            200: PartialAdminUserSerializer(many=True),
        },
    )
    @validate_body(PartialAdminUserSerializer, partial=True)
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def patch(self, request, user_id, data):
        """Edits a user"""

        handler = UserAdminHandler()
        user = handler.update_user(request.user, user_id, data)

        return Response(PartialAdminUserSerializer(user).data)

    @extend_schema(
        tags=["Admin"],
        operation_id="delete_users_admin",
        description="TODO",
        responses={200},
    )
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
        }
    )
    def delete(self, request, user_id):
        """Deletes a a user."""

        handler = UserAdminHandler()
        handler.delete_user(request.user, user_id)

        return Response()
