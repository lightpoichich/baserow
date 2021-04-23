from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.fields import (
    SerializerMethodField,
    BooleanField,
    EmailField,
    CharField,
)
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
    full_name = CharField(source="first_name")
    groups = GroupSerializer(source="group_set", many=True)

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
    full_name = CharField(min_length=2, allow_null=True)
    is_active = BooleanField(allow_null=True)
    is_staff = BooleanField(allow_null=True)
    username = EmailField(allow_null=True)
    password = CharField(write_only=True, max_length=256, allow_null=True)

    def __init__(self, *args, **kwargs):
        kwargs["partial"] = True
        super().__init__(*args, **kwargs)


class UsersAdminView(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin"],
        operation_id="list_users_admin",
        description="TODO",
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
        description="TODO",
        responses={
            200: AdminUserSerializer(many=True),
        },
    )
    def patch(self, request, user_id):
        """Edits a user"""

        handler = UserAdminHandler()
        print(request.data)
        data = validate_data(AdminUserUpdateSerializer, request.data)
        print(data)
        user = handler.update_user(user_id, data)

        return Response(AdminUserSerializer(user).data)

    @extend_schema(
        tags=["Admin"],
        operation_id="delete_users_admin",
        description="TODO",
        responses={200},
    )
    def delete(self, request, user_id):
        """Deletes a a user."""

        handler = UserAdminHandler()
        handler.delete_user(user_id)

        return Response()
