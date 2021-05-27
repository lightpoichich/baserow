from drf_spectacular.utils import extend_schema

from baserow.core.models import Group

from baserow_premium.api.admin.views import AdminListingView

from .serializers import GroupsAdminResponseSerializer


class GroupsAdminView(AdminListingView):
    serializer_class = GroupsAdminResponseSerializer
    search_fields = ["id", "name"]
    sort_field_mapping = {"id": "id", "name": "name", "created_on": "created_on"}

    def get_queryset(self, request):
        return Group.objects.prefetch_related("groupuser_set", "groupuser_set__user")

    @extend_schema(
        tags=["Admin"],
        operation_id="list_groups",
        description="Returns all users with detailed information on each user, "
        "if the requesting user has admin permissions.",
        **AdminListingView.get_extend_schema_parameters(
            "groups", serializer_class, search_fields, sort_field_mapping
        ),
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
