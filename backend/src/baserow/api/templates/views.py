from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from baserow.api.templates.serializers import TemplateCategoriesSerializer
from baserow.core.models import TemplateCategory


class TemplatesView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['Templates'],
        operation_id='list_templates',
        description=(
            'Lists all the template categories and the related templates that are in '
            'that category. The `group_id` can be used for previewing purposes. All '
            'the `get` and `list`endpoints are publicly accessible if the group is '
            'related to a template.'
        ),
        responses={
            200: TemplateCategoriesSerializer(many=True)
        }
    )
    def get(self, request):
        """Responds with a list of template categories and templates."""

        categories = TemplateCategory.objects.all().prefetch_related('templates')
        serializer = TemplateCategoriesSerializer(categories, many=True)
        return Response(serializer.data)
