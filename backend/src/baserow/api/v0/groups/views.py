from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from baserow.core.models import GroupUser

from .serializers import GroupUserSerializer


class GroupsView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def get(self, request):
        groups = GroupUser.objects.filter(user=request.user).select_related('group')
        serializer = GroupUserSerializer(groups, many=True)
        return Response(serializer.data)
