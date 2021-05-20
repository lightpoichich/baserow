from datetime import timedelta

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from baserow.core.models import Group, Application
from baserow_premium.admin_dashboard.handler import AdminDashboardHandler

from .serializers import AdminDashboardSerializer


User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin dashboard"],
        operation_id="admin_dashboard",
        description="@TODO",
        responses={
            200: AdminDashboardSerializer,
        },
    )
    def get(self, request):
        """
        @TODO
        """

        handler = AdminDashboardHandler()
        total_users = User.objects.filter(is_active=True).count()
        total_groups = Group.objects.all().count()
        total_applications = Application.objects.all().count()
        new_users = handler.get_new_user_counts(
            {
                "new_users_last_24_hours": timedelta(hours=24),
                "new_users_last_7_days": timedelta(days=7),
                "new_users_last_30_days": timedelta(days=30),
            },
            include_previous=True,
        )
        active_users = handler.get_active_user_count(
            {
                "active_users_last_24_hours": timedelta(hours=24),
                "active_users_last_7_days": timedelta(days=7),
                "active_users_last_30_days": timedelta(days=30),
            },
            include_previous=True,
        )
        new_users_per_day = handler.get_new_user_count_per_day(timedelta(days=30))
        active_users_per_day = handler.get_active_user_count_per_day(timedelta(days=30))

        serializer = AdminDashboardSerializer(
            {
                "total_users": total_users,
                "total_groups": total_groups,
                "total_applications": total_applications,
                "new_users_per_day": new_users_per_day,
                "active_users_per_day": active_users_per_day,
                **new_users,
                **active_users,
            }
        )
        return Response(serializer.data)
