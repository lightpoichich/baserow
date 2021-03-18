from django.db.models import Q, BooleanField
from django.db.models.expressions import RawSQL
from typing import Union, Any, Dict, Tuple, Optional

FieldFilterWithAnnotation = Tuple[Q, Optional[Dict[str, Any]]]
FieldFilter = Union[Q, FieldFilterWithAnnotation]


def unpack_field_filter(field_filter: FieldFilter) -> FieldFilterWithAnnotation:
    if isinstance(field_filter, tuple):
        return field_filter
    else:
        return field_filter, None


def contains_filter(field_name, value, model_field, _) -> FieldFilter:
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


def filename_contains_filter(field_name, value, _, field) -> FieldFilter:
    value = value.strip()
    # If an empty value has been provided we do not want to filter at all.
    if value == '':
        return Q()
    # Check if the model_field has a file which matches the provided filter value.
    filename_filter = Q(**{f'{field_name}_matches_visible_names': True})
    annotation_query = _build_filename_contains_raw_query(field, value)
    return filename_filter, {f'{field_name}_matches_visible_names': annotation_query}


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
