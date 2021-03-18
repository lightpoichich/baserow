from typing import Dict, Any, Union

from django.db.models import Q, BooleanField
from django.db.models.expressions import RawSQL

FILTER_TYPE_AND = 'AND'
FILTER_TYPE_OR = 'OR'


class AnnotatedQ(Q):
    """
    A simple wrapper class adding a annotation attribute to the django Q class.
    WARNING: This will not automatically apply the provided annotation when used in a
    queryset, you must used the FilterBuilder class which will use these extra
    annotations when building a queryset.
    """

    def __init__(self, annotation: Dict[str, Any], *args, **kwargs):
        """
        :param annotation: A dictionary which can be unpacked into a django
        Queryset.annotate call. This will only happen when using
        FilterBuilder.apply_to_queryset.
        :param kwargs: kwargs which will be passed to Q as normal.
        """
        self.annotation = annotation or {}
        super().__init__(*args, **kwargs)


OptionallyAnnotatedQ = Union[Q, AnnotatedQ]


class FilterBuilder:
    """
    Combines together multiple Q or AnnotatedQ filters into a single filter which
    can either AND or OR the provided filters together based on the filter_type
    parameter. Additionally it will annotate the filtered queryset with any provided
    annotations from AnnotatedQ filters.
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

    def combine(self, q: OptionallyAnnotatedQ) -> 'FilterBuilder':
        if isinstance(q, AnnotatedQ):
            self.annotate(q.annotation)
            self.filter(q)
        else:
            self.filter(q)
        return self

    def apply_to_queryset(self, queryset):
        return queryset.annotate(**self.annotation).filter(self.q_filters)


def contains_filter(field_name, value, model_field, _) -> OptionallyAnnotatedQ:
    value = value.strip()
    # If an empty value has been provided we do not want to filter at all.
    if value == '':
        return Q()
    # Check if the model_field accepts the value.
    try:
        model_field.get_prep_value(value)
        return Q(**{f'{field_name}__icontains': value})
    except Exception:
        pass
    return Q()


def filename_contains_filter(field_name, value, _, field) -> OptionallyAnnotatedQ:
    value = value.strip()
    # If an empty value has been provided we do not want to filter at all.
    if value == '':
        return Q()
    # Check if the model_field has a file which matches the provided filter value.
    annotation_query = _build_filename_contains_raw_query(field, value)
    annotation = {f'{field_name}_matches_visible_names': annotation_query}
    return AnnotatedQ(annotation=annotation,
                      **{f'{field_name}_matches_visible_names': True})


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
