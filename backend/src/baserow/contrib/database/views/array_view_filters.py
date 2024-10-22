import typing

from django.db.models import BooleanField, F, Q, Value

from loguru import logger

from baserow.contrib.database.fields.field_filters import (
    AnnotatedQ,
    OptionallyAnnotatedQ,
)
from baserow.contrib.database.fields.field_types import FormulaFieldType
from baserow.contrib.database.fields.filter_support import (
    FilterNotSupportedException,
    HasValueContainsFilterSupport,
    HasValueContainsWordFilterSupport,
    HasValueEmptyFilterSupport,
    HasValueFilterSupport,
    HasValueLengthIsLowerThanFilterSupport,
)
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.formula import BaserowFormulaTextType
from baserow.contrib.database.formula.expression_generator.django_expressions import (
    BaserowFilterExpression,
    JSONArrayAllAreExpr,
    JSONArrayAnyIsExpr,
    JSONArrayNoneIsExpr,
)
from baserow.contrib.database.formula.types.formula_types import (
    BaserowFormulaBooleanType,
    BaserowFormulaCharType,
    BaserowFormulaURLType,
)

from .registries import ViewFilterType
from .view_filters import NotViewFilterTypeMixin


class HasEmptyValueViewFilterType(ViewFilterType):
    """
    The filter can be used to check for empty condition for
    items in an array.
    """

    type = "has_empty_value"
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaTextType.type),
            FormulaFieldType.array_of(BaserowFormulaCharType.type),
            FormulaFieldType.array_of(BaserowFormulaURLType.type),
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            field_type = field_type_registry.get_by_model(field)

            if not isinstance(field_type, HasValueEmptyFilterSupport):
                raise FilterNotSupportedException()

            return field_type.get_in_array_empty_query(field_name, model_field, field)
        except Exception:
            return self.default_filter_on_exception()


class HasNotEmptyValueViewFilterType(
    NotViewFilterTypeMixin, HasEmptyValueViewFilterType
):
    type = "has_not_empty_value"


class HasValueEqualViewFilterType(ViewFilterType):
    """
    The filter can be used to check for "is" condition for
    items in an array.
    """

    type = "has_value_equal"
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaTextType.type),
            FormulaFieldType.array_of(BaserowFormulaCharType.type),
            FormulaFieldType.array_of(BaserowFormulaURLType.type),
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            field_type = field_type_registry.get_by_model(field)

            if not isinstance(field_type, HasValueFilterSupport):
                raise FilterNotSupportedException()

            return field_type.get_in_array_is_query(
                field_name, value, model_field, field
            )
        except Exception:
            return self.default_filter_on_exception()


class HasNotValueEqualViewFilterType(
    NotViewFilterTypeMixin, HasValueEqualViewFilterType
):
    type = "has_not_value_equal"


class HasValueContainsViewFilterType(ViewFilterType):
    """
    The filter can be used to check for "contains" condition for
    items in an array.
    """

    type = "has_value_contains"
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaTextType.type),
            FormulaFieldType.array_of(BaserowFormulaCharType.type),
            FormulaFieldType.array_of(BaserowFormulaURLType.type),
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            field_type = field_type_registry.get_by_model(field)

            if not isinstance(field_type, HasValueContainsFilterSupport):
                raise FilterNotSupportedException()

            return field_type.get_in_array_contains_query(
                field_name, value, model_field, field
            )
        except Exception:
            return self.default_filter_on_exception()


class HasNotValueContainsViewFilterType(
    NotViewFilterTypeMixin, HasValueContainsViewFilterType
):
    type = "has_not_value_contains"


class HasValueContainsWordViewFilterType(ViewFilterType):
    """
    The filter can be used to check for "contains word" condition
    for items in an array.
    """

    type = "has_value_contains_word"
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaTextType.type),
            FormulaFieldType.array_of(BaserowFormulaCharType.type),
            FormulaFieldType.array_of(BaserowFormulaURLType.type),
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            field_type = field_type_registry.get_by_model(field)

            if not isinstance(field_type, HasValueContainsWordFilterSupport):
                raise FilterNotSupportedException()

            return field_type.get_in_array_contains_word_query(
                field_name, value, model_field, field
            )
        except Exception:
            return self.default_filter_on_exception()


class HasNotValueContainsWordViewFilterType(
    NotViewFilterTypeMixin, HasValueContainsWordViewFilterType
):
    type = "has_not_value_contains_word"


class HasValueLengthIsLowerThanViewFilterType(ViewFilterType):
    """
    The filter can be used to check for "length is lower than" condition
    for items in an array.
    """

    type = "has_value_length_is_lower_than"
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaTextType.type),
            FormulaFieldType.array_of(BaserowFormulaCharType.type),
            FormulaFieldType.array_of(BaserowFormulaURLType.type),
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            field_type = field_type_registry.get_by_model(field)

            if not isinstance(field_type, HasValueLengthIsLowerThanFilterSupport):
                raise FilterNotSupportedException()

            return field_type.get_in_array_length_is_lower_than_query(
                field_name, value, model_field, field
            )
        except Exception:
            return self.default_filter_on_exception()


class _OfArrayIsMixin:
    json_expression: typing.ClassVar[typing.Type[BaserowFilterExpression]]
    compatible_field_types = [
        FormulaFieldType.compatible_with_formula_types(
            FormulaFieldType.array_of(BaserowFormulaBooleanType.type)
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        try:
            value = value.strip()
            if not value:
                return Q()
            converted_value = True if value == "1" else False
            annotation_query = self.json_expression(
                F(field_name), Value(converted_value), output_field=BooleanField()
            )
            hashed_value = hash(value)
            return AnnotatedQ(
                annotation={
                    f"{field_name}_none_of_array_is_{hashed_value}": annotation_query
                },
                q={f"{field_name}_none_of_array_is_{hashed_value}": True},
            )
        except Exception as err:
            logger.error(
                f"Error when creating {self.type} filter expression for {field_name} field with {value} value: {err}"
            )
            return self.default_filter_on_exception()


class NoneOfArrayIsViewFilterType(_OfArrayIsMixin, ViewFilterType):
    type = "none_of_array_is"
    json_expression = JSONArrayNoneIsExpr


class AnyOfArrayIsViewFilterType(_OfArrayIsMixin, ViewFilterType):
    type = "any_of_array_is"
    json_expression = JSONArrayAnyIsExpr


class AllOfArrayAreViewFilterType(_OfArrayIsMixin, ViewFilterType):
    type = "all_of_array_are"
    json_expression = JSONArrayAllAreExpr
