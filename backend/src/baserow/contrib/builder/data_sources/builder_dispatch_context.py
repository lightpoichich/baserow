from functools import cached_property
from typing import TYPE_CHECKING, Dict, List, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpRequest

from baserow.contrib.builder.data_providers.registries import (
    builder_data_provider_type_registry,
)
from baserow.contrib.builder.data_sources.exceptions import (
    DataSourceRefinementForbidden,
)
from baserow.contrib.builder.formula_property_extractor import get_formula_field_names
from baserow.contrib.builder.pages.models import Page
from baserow.core.feature_flags import feature_flag_is_enabled
from baserow.core.services.dispatch_context import DispatchContext
from baserow.core.services.utils import ServiceAdhocRefinements

if TYPE_CHECKING:
    from baserow.contrib.builder.elements.models import CollectionElement
    from baserow.core.workflow_actions.models import WorkflowAction

FEATURE_FLAG_EXCLUDE_UNUSED_FIELDS = "feature-exclude-unused-fields"

User = get_user_model()


class BuilderDispatchContext(DispatchContext):
    own_properties = [
        "request",
        "page",
        "workflow_action",
        "element",
        "offset",
        "count",
        "only_expose_public_formula_fields",
    ]

    def __init__(
        self,
        request: HttpRequest,
        page: Page,
        workflow_action: Optional["WorkflowAction"] = None,
        element: Optional["CollectionElement"] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
        only_expose_public_formula_fields: Optional[bool] = True,
    ):
        self.request = request
        self.page = page
        self.workflow_action = workflow_action
        self.element = element

        # Overrides the `request` GET offset/count values.
        self.offset = offset
        self.count = count
        self.only_expose_public_formula_fields = only_expose_public_formula_fields

        super().__init__()

    @property
    def data_provider_registry(self):
        return builder_data_provider_type_registry

    def get_cache_key(self) -> Optional[str]:
        """
        Returns a cache key that can be used to key the results of making the
        expensive function call to get_formula_field_names().

        If the user is a Django user, return None. This is because the Page
        Designer should always have the latest data in the Preview (e.g. when
        they are not authenticated). Also, the Django user doesn't have the role
        attribute, unlike the User Source User.
        """

        if isinstance(self.request.user, User):
            return None
        elif self.request.user.is_anonymous:
            role = "anonymous"
        else:
            role = self.request.user.role

        return f"{self.page.id}_{role}"

    @cached_property
    def public_formula_fields(self) -> Optional[Dict[str, Dict[int, List[str]]]]:
        """
        Return a Dict where keys are ["all", "external", "internal"] and values
        dicts. The internal dicts' keys are Service IDs and values are a list
        of Data Source field names.

        Returns None if field names shouldn't be included in the dispatch
        context. This is mainly to support a feature flag for this new feature.

        The field names are used to improve the security of the backend by
        ensuring only the minimum necessary data is exposed to the frontend.

        It is used to restrict the queryset as well as to discern which Data
        Source fields are external and safe (user facing) vs internal and
        sensitive (required only by the backend).
        """

        if self.only_expose_public_formula_fields and feature_flag_is_enabled(
            FEATURE_FLAG_EXCLUDE_UNUSED_FIELDS
        ):
            cache_key = self.get_cache_key()

            formula_fields = cache.get(cache_key) if cache_key else None
            if formula_fields is None:
                formula_fields = get_formula_field_names(self.request.user, self.page)
            
                if cache_key:
                    cache.set(
                        cache_key,
                        formula_fields,
                        timeout=settings.PUBLIC_FORMULA_FIELDS_CACHE_TTL_SECONDS,
                    )

            return formula_fields

        return None

    def range(self, service):
        """
        Return page range from the `offset`, `count` kwargs,
        or the GET parameters.
        """

        if self.offset is not None and self.count is not None:
            offset = self.offset
            count = self.count
        else:
            try:
                offset = int(self.request.GET.get("offset", 0))
            except ValueError:
                offset = 0

            try:
                count = int(self.request.GET.get("count", 20))
            except ValueError:
                count = 20

        # max prevent negative values
        return [
            max(0, offset),
            max(1, count),
        ]

    def get_element_property_options(self) -> Dict[str, Dict[str, bool]]:
        """
        Responsible for returning the property options for the element.
        The property options are cached if they haven't already been, so
        that they can be re-used by other methods.

        :raises DataSourceRefinementForbidden: If `self.element` is `None`.
        """

        if not self.element:
            raise DataSourceRefinementForbidden(
                "An element is required to validate filter, search and sort fields."
            )

        if "element_property_options" not in self.cache:
            self.cache["element_property_options"] = {
                po.schema_property: {
                    "filterable": po.filterable,
                    "sortable": po.sortable,
                    "searchable": po.searchable,
                }
                for po in self.element.property_options.all()
            }

        return self.cache["element_property_options"]

    def search_query(self) -> Optional[str]:
        """
        In a `BuilderDispatchContext`, we will use the HTTP request
        to return the `search_query` provided by the frontend.

        :return: A search query string.
        """

        return self.request.GET.get("search_query", None)

    def searchable_fields(self) -> Optional[List[str]]:
        """
        In a `BuilderDispatchContext`, we will use the `element` to
        determine which fields are searchable, by checking the `property_options`.

        :raises: DataSourceRefinementForbidden: If `self.element` is `None`.
        :return: A list of searchable fields.
        """

        property_options = self.get_element_property_options()
        return [
            schema_property
            for schema_property, options in property_options.items()
            if options["searchable"]
        ]

    def filters(self) -> Optional[str]:
        """
        In a `BuilderDispatchContext`, we will use the HTTP request's
        serialized `filters`, pass it to the `AdHocFilters` class, and
        return the result.

        :return: A JSON serialized string.
        """

        return self.request.GET.get("filters", None)

    def sortings(self) -> Optional[str]:
        """
        In a `BuilderDispatchContext`, we will use the HTTP request
        to return the `order_by` provided by the frontend.

        :return: A sort string.
        """

        return self.request.GET.get("order_by", None)

    def validate_filter_search_sort_fields(
        self, fields: List[str], refinement: ServiceAdhocRefinements
    ):
        """
        Responsible for ensuring that all fields present in `fields`
        are allowed as a refinement for the given `refinement`. For example,
        if the `refinement` is `FILTER`, then all fields in `fields` need
        to be filterable.

        :param fields: The fields to validate.
        :param refinement: The refinement to validate.
        :raises DataSourceRefinementForbidden: If a field is not allowed for the given
            refinement.
        """

        # Get the property options for the element.
        property_options = self.get_element_property_options()

        # The filterable/sortable/searchable options for the given fields.
        # If a `field` has been provided that doesn't exist in the property options
        # table, it means it hasn't been configured by the page designer, so all
        # three refinement options are disabled.
        field_property_options = {
            schema_property: property_options.get(
                schema_property,
                {"filterable": False, "sortable": False, "searchable": False},
            )
            for schema_property in fields
        }

        for field_property, field_options in field_property_options.items():
            # If the property is not allowed for the given refinement, raise an error.
            model_field = ServiceAdhocRefinements.to_model_field(refinement)
            if not field_options[model_field]:
                raise DataSourceRefinementForbidden(
                    f"{field_property} is not a {model_field} field."
                )
