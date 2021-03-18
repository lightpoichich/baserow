from baserow.core.registry import (
    Instance, Registry, ModelInstanceMixin, ModelRegistryMixin,
    CustomFieldsInstanceMixin, CustomFieldsRegistryMixin, APIUrlsRegistryMixin,
    APIUrlsInstanceMixin
)
from .exceptions import (
    ViewTypeAlreadyRegistered, ViewTypeDoesNotExist, ViewFilterTypeAlreadyRegistered,
    ViewFilterTypeDoesNotExist
)
from ..fields.field_filters import FieldFilter


class ViewType(APIUrlsInstanceMixin, CustomFieldsInstanceMixin, ModelInstanceMixin,
               Instance):
    """
    This abstract class represents a custom view type that can be added to the
    view type registry. It must be extended so customisation can be done. Each view type
    will have his own model that must extend the View model, this is needed so that the
    user can set custom settings per view instance he has created.

    The added API urls will be available under the namespace 'api:database:views'.
    So if a url with name 'example' is returned by the method it will available under
    reverse('api:database:views:example').

    Example:
        from baserow.contrib.database.views.models import View
        from baserow.contrib.database.views.registry import ViewType, view_type_registry

        class ExampleViewModel(ViewType):
            pass

        class ExampleViewType(ViewType):
            type = 'unique-view-type'
            model_class = ExampleViewModel
            allowed_fields = ['example_ordering']
            serializer_field_names = ['example_ordering']
            serializer_field_overrides = {
                'example_ordering': serializers.CharField()
            }

            def get_api_urls(self):
                return [
                    path('view-type/', include(api_urls, namespace=self.type)),
                ]

        view_type_registry.register(ExampleViewType())
    """

    can_filter = True
    """
    Indicates if the view supports filters. If not, it will not be possible to add
    filter to the view.
    """

    can_sort = True
    """
    Indicates if the view support sortings. If not, it will not be possible to add a
    sort to the view.
    """


class ViewTypeRegistry(APIUrlsRegistryMixin, CustomFieldsRegistryMixin,
                       ModelRegistryMixin, Registry):
    """
    With the view type registry it is possible to register new view types.  A view type
    is an abstraction made specifically for Baserow. If added to the registry a user can
    create new views based on this type.
    """

    name = 'view'
    does_not_exist_exception_class = ViewTypeDoesNotExist
    already_registered_exception_class = ViewTypeAlreadyRegistered


class ViewFilterType(Instance):
    """
    This abstract class represents a view filter type that can be added to the view
    filter type registry. It must be extended so customisation can be done. Each view
    filter type will have its own type names and rules. The get_filter method should
    be overwritten and should return a Q object that can be applied to the queryset
    later.

    Example:
        from baserow.contrib.database.views.registry import (
            ViewFilterType, view_filter_type_registry
        )

        class ExampleViewFilterType(ViewFilterType):
            type = 'equal'
            compatible_field_types = ['text', 'long_text']

            def get_filter(self, field_name, value):
                return Q(**{
                    field_name: value
                })

        view_filter_type_registry.register(ExampleViewFilterType())
    """

    compatible_field_types = []
    """
    Defines which field types are compatible with the filter. Only the supported ones
    can be used in combination with the field.
    """

    def get_filter(self, field_name, value, model_field, field) -> FieldFilter:
        """
        Should return a Q object containing the requested filtering based on the
        provided arguments. It can additionally return an annotations dictionary to
        enhance the queryset for use in the filter for more powerful filtering logic.

        :param field_name: The name of the field that needs to be filtered.
        :type field_name: str
        :param value: The value that the field must be compared to.
        :type value: str
        :param model_field: The field extracted from the model.
        :type model_field: models.Field
        :param field: The instance of the underlying baserow field.
        :type field: Field
        :return: The Q object that does the filtering. This will later be added to the
            queryset in the correct way. Or a tuple with the first element being the
            Q object and the second being a dictionary which will be unpacked into an
            annotate call on the view filters queryset prior to the Q object being
            applied as a filter.
        """

        raise NotImplementedError('Each must have his own get_filter method.')


class ViewFilterTypeRegistry(Registry):
    """
    With the view filter type registry is is possible to register new view filter
    types. A view filter type is an abstractions that allows different types of
    filtering for rows in a view. It is possible to add multiple view filters to a view
    and all the rows must match those filters.
    """

    name = 'view_filter'
    does_not_exist_exception_class = ViewFilterTypeDoesNotExist
    already_registered_exception_class = ViewFilterTypeAlreadyRegistered


# A default view type registry is created here, this is the one that is used
# throughout the whole Baserow application to add a new view type.
view_type_registry = ViewTypeRegistry()
view_filter_type_registry = ViewFilterTypeRegistry()
