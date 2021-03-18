from typing import Optional, Dict, Any, Union

from django.db.models import Q, BooleanField
from django.db.models.expressions import RawSQL

FILTER_TYPE_AND = 'AND'
FILTER_TYPE_OR = 'OR'


class CombinableFilter:
    """
    A simple wrapper class providing a fluent interface for specifying a filter that
    can also contain an annotation.

    Multiple sub types are used here to ensure that the user of this class never
    accidentally uses the Api with multiple annotations or multiple filters, e.g.:
    annotate_combinable(...).annotate(...)  will show up as a type error when
    the programmer writes the invalid code, which is much preferable to them
    discovering the error at runtime.
    """

    def __init__(self, q_filter: Optional[Q], annotation: Optional[Dict[str, Any]]):
        self.annotation = annotation or {}
        self.q_filter = q_filter or Q()

    def __invert__(self) -> 'CombinableFilter':
        return CombinableFilter(~self.q_filter, self.annotation)


class _CombinableFilterWithBoth(CombinableFilter):
    def __init__(self, q_filter, annotation):
        super().__init__(q_filter, annotation)


class _CombinableFilterWithFilter(CombinableFilter):
    def __init__(self, q_filter):
        super().__init__(q_filter, None)

    def annotate(self, annotation) -> '_CombinableFilterWithBoth':
        return _CombinableFilterWithBoth(self.q_filter, annotation)


class _CombinableFilterWithAnnotation(CombinableFilter):
    def __init__(self, annotation):
        super().__init__(None, annotation)

    def filter(self, q_filter) -> '_CombinableFilterWithBoth':
        return _CombinableFilterWithBoth(q_filter, self.annotation)


def annotate_combinable(annotation) -> '_CombinableFilterWithAnnotation':
    return _CombinableFilterWithAnnotation(annotation)


def filter_combinable(q_filter) -> '_CombinableFilterWithFilter':
    return _CombinableFilterWithFilter(q_filter)


def no_filter_combinable() -> 'CombinableFilter':
    return CombinableFilter(None, None)


class FilterBuilder:
    """
    Combines together multiple CombinableFilters into a single filter which can either
    AND or OR the provided Q filters together based on the filter_type parameter.
    """

    def __init__(self, filter_type):
        self.annotation = {}
        self.q_filters = Q()
        self.filter_type = filter_type

    def annotate(self, annotation_dict: Dict[str, Any]) -> 'FilterBuilder':
        self.annotation = {**self.annotation, **annotation_dict}
        return self

    def filter(self, q_filter: Q) -> 'FilterBuilder':
        if self.filter_type == FILTER_TYPE_AND:
            self.q_filters &= q_filter
        elif self.filter_type == FILTER_TYPE_OR:
            self.q_filters |= q_filter
        else:
            raise ValueError(f'Unknown filter type {self.filter_type}.')
        return self

    def combine(self, combinable_filter: Union[CombinableFilter, Q]) -> 'FilterBuilder':
        if isinstance(combinable_filter, CombinableFilter):
            self.annotate(combinable_filter.annotation)
            self.filter(combinable_filter.q_filter)
        else:
            self.filter(combinable_filter)
        return self

    def apply_to_queryset(self, queryset):
        return queryset.annotate(**self.annotation).filter(self.q_filters)


def contains_filter(field_name, value, model_field, _) -> CombinableFilter:
    value = value.strip()
    # If an empty value has been provided we do not want to filter at all.
    if value == '':
        return no_filter_combinable()
    # Check if the model_field accepts the value.
    try:
        model_field.get_prep_value(value)
        return filter_combinable(Q(**{f'{field_name}__icontains': value}))
    except Exception:
        pass
    return no_filter_combinable()


def filename_contains_filter(field_name, value, _, field) -> CombinableFilter:
    value = value.strip()
    # If an empty value has been provided we do not want to filter at all.
    if value == '':
        return no_filter_combinable()
    # Check if the model_field has a file which matches the provided filter value.
    filename_filter = Q(**{f'{field_name}_matches_visible_names': True})
    annotation_query = _build_filename_contains_raw_query(field, value)
    annotation = {f'{field_name}_matches_visible_names': annotation_query}
    return annotate_combinable(annotation).filter(filename_filter)


def _build_filename_contains_raw_query(field, value):
    # It is not possible to use Django's ORM to query for if one item in a JSONB
    # list has has a key which contains a specified value.
    #
    # The closest thing the Django ORM provides is:
    #   queryset.filter(your_json_field__contains=[{"key":"value"}])
    # However this is an exact match, so in the above example [{"key":"value_etc"}]
    # would not match the filter.
    #
    # Instead we have to resort to RawSQL to use various built in PostgreSQL JSON
    # Array manipulation functions to be able to 'iterate' over a JSONB list
    # performing `like` on individual keys in said list.
    num_files_with_name_like_value = f"""
        EXISTS(
            SELECT attached_files ->> 'visible_name'
            FROM JSONB_ARRAY_ELEMENTS("field_{field.id}") as attached_files
            WHERE UPPER(attached_files ->> 'visible_name') LIKE UPPER(%s)
        )
    """
    return RawSQL(num_files_with_name_like_value, params=[f"%{value}%"],
                  output_field=BooleanField())
