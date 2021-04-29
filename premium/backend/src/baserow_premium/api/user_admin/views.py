from typing import List, Optional

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.decorators import validate_body, map_exceptions
from baserow.api.pagination import PageNumberPagination
from baserow.api.schemas import get_error_schema
from baserow_premium.api.user_admin.errors import (
    ERROR_ADMIN_ONLY_OPERATION,
    InvalidSortDirectionException,
    INVALID_SORT_DIRECTION,
    INVALID_SORT_ATTRIBUTE,
    InvalidSortAttributeException,
)
from baserow_premium.api.user_admin.serializers import AdminUserSerializer
from baserow_premium.user_admin.exceptions import (
    AdminOnlyOperationException,
)
from baserow_premium.user_admin.handler import (
    UserAdminHandler,
    UserAdminSort,
    SortableUserAdminField,
)


class UsersAdminView(APIView):
    _valid_sortable_fields = ",".join(
        [f"`{f.value}`" for f in list(SortableUserAdminField)]
    )

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
                name="sorts",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="A comma separated string of user attributes to sort by, "
                "each attribute must be prefixed with `+` for a descending "
                "sort or a `-` for an ascending sort. The accepted attribute names "
                f"are: {_valid_sortable_fields}.",
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
                    "INVALID_SORT_DIRECTION",
                    "INVALID_SORT_ATTRIBUTE",
                ]
            ),
            401: get_error_schema(["ERROR_ADMIN_ONLY_OPERATION"]),
        },
    )
    @map_exceptions(
        {
            AdminOnlyOperationException: ERROR_ADMIN_ONLY_OPERATION,
            InvalidSortDirectionException: INVALID_SORT_DIRECTION,
            InvalidSortAttributeException: INVALID_SORT_ATTRIBUTE,
        }
    )
    def get(self, request):
        """
        Lists all the users of a user, optionally filtering on username by the
        'search' get parameter, optionally sorting by the 'sorts' get parameter.
        """

        search = request.GET.get("search")
        sorts_param = request.GET.get("sorts")

        handler = UserAdminHandler()
        sorts = self.parse_sorts(sorts_param)
        users = handler.get_users(request.user, search, sorts)

        paginator = PageNumberPagination(limit_page_size=100)
        page = paginator.paginate_queryset(users, request, self)
        serializer = AdminUserSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    def parse_sorts(sorts: Optional[str]) -> List[UserAdminSort]:
        """
        Parses an optional comma separated string into a list of user sorts. Each item
        in the string must either begin with a + for a ascending sort or a - for a
        descending sort. Following the + or - a valid field name to sort must be
        provided. The valid field names are the values of the baserow_premium.user_admin
        .handler.SortableUserField enum.

        :param sorts: An optional comma separated string of user sorts.
        :return: A list of valid user sorts.
        """
        if sorts is None:
            return []
        parsed_sorts = []
        for s in sorts.split(","):
            if len(s) <= 2:
                raise InvalidSortAttributeException()

            sort_direction_prefix = s[0]
            sort_field_name = s[1:]

            if sort_direction_prefix not in ["-", "+"]:
                raise InvalidSortDirectionException()

            try:
                field = SortableUserAdminField(sort_field_name)
            except KeyError:
                raise InvalidSortAttributeException()

            is_descending_sort = sort_direction_prefix == "-"
            parsed_sorts.append(UserAdminSort(is_descending_sort, field))
        return parsed_sorts


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
