from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ModelSerializer

from baserow.api.groups.serializers import GroupSerializer
from baserow.api.pagination import PageNumberPagination

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


class UserAdminView(ListAPIView):
    permission_classes = (IsAdminUser,)
    pagination_class = PageNumberPagination
    serializer_class = AdminUserSerializer
    queryset = User.objects.order_by("id").all()
