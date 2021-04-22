from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.fields import SerializerMethodField, BooleanField
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from baserow.api.groups.serializers import GroupSerializer
from baserow.api.pagination import PageNumberPagination
from baserow.api.utils import validate_data
from baserow.contrib.database.api.tokens.authentications import TokenAuthentication
from baserow_premium.handler import UserAdminHandler

User = get_user_model()


class AdminUserSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    groups = GroupSerializer(source="group_set", many=True)

    # noinspection PyMethodMayBeStatic
    def get_full_name(self, obj):
        return obj.first_name + obj.last_name

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "groups",
            "last_login",
            "date_joined",
            "is_active",
            "is_staff",
        )


class AdminUserUpdateSerializer(Serializer):
    is_active = BooleanField()


class UsersAdminView(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin"],
        operation_id="list_users_admin",
        description=(
            "Lists all the API users that belong to the authorized user. An API token "
            "can be used to create, read, update and delete rows in the tables of the "
            "token's group. It only works on the tables if the token has the correct "
            "permissions. The **Database table rows** endpoints can be used for these "
            "operations."
        ),
        responses={
            200: AdminUserSerializer(many=True),
        },
    )
    def get(self, request):
        """Lists all the users of a user."""

        handler = UserAdminHandler()
        users = handler.get_users()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(users, request, self)
        serializer = AdminUserSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class UserAdminView(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin"],
        operation_id="edit_users_admin",
        description=(
            "Lists all the API users that belong to the authorized user. An API token "
            "can be used to create, read, update and delete rows in the tables of the "
            "token's group. It only works on the tables if the token has the correct "
            "permissions. The **Database table rows** endpoints can be used for these "
            "operations."
        ),
        responses={
            200: AdminUserSerializer(many=True),
        },
    )
    def patch(self, request, user_id):
        """Edits a user"""

        handler = UserAdminHandler()
        data = validate_data(AdminUserUpdateSerializer, request.data)
        user = handler.update_user(user_id, data)

        return Response(AdminUserSerializer(user).data)

    @extend_schema(
        tags=["Admin"],
        operation_id="delete_users_admin",
        description=(
            "Lists all the API users that belong to the authorized user. An API token "
            "can be used to create, read, update and delete rows in the tables of the "
            "token's group. It only works on the tables if the token has the correct "
            "permissions. The **Database table rows** endpoints can be used for these "
            "operations."
        ),
        responses={200},
    )
    def delete(self, request, user_id):
        """Deletes a a user."""

        handler = UserAdminHandler()
        handler.delete_user(user_id)

        return Response()
