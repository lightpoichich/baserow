from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.db.models import Value

from baserow_premium.api.fields.exceptions import (
    ERROR_GENERATIVE_AI_DOES_NOT_SUPPORT_FILE_FIELD,
)
from baserow_premium.fields.exceptions import GenerativeAITypeDoesNotSupportFileField
from rest_framework import serializers

from baserow.api.generative_ai.errors import (
    ERROR_GENERATIVE_AI_DOES_NOT_EXIST,
    ERROR_MODEL_DOES_NOT_BELONG_TO_TYPE,
)
from baserow.contrib.database.api.fields.errors import ERROR_FIELD_DOES_NOT_EXIST
from baserow.contrib.database.fields.field_filters import (
    contains_filter,
    contains_word_filter,
)
from baserow.contrib.database.fields.field_types import CollationSortMixin, TextField
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.fields.registries import FieldType
from baserow.contrib.database.formula import BaserowFormulaTextType, BaserowFormulaType
from baserow.core.db import collate_expression
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.generative_ai.exceptions import (
    GenerativeAITypeDoesNotExist,
    ModelDoesNotBelongToType,
)
from baserow.core.generative_ai.registries import (
    GenerativeAIWithFilesModelType,
    generative_ai_model_type_registry,
)

from .models import AIField
from .visitors import replace_field_id_references

User = get_user_model()

if TYPE_CHECKING:
    from baserow.contrib.database.table.models import GeneratedTableModel


class AIFieldType(CollationSortMixin, FieldType):
    """
    The AI field can automatically query a generative AI model based on the provided
    prompt. It's possible to reference other fields to generate a unique output.
    """

    type = "ai"
    model_class = AIField
    can_be_in_form_view = False
    keep_data_on_duplication = True
    allowed_fields = [
        "ai_generative_ai_type",
        "ai_generative_ai_model",
        "ai_prompt",
        "ai_file_field_id",
    ]
    serializer_field_names = [
        "ai_generative_ai_type",
        "ai_generative_ai_model",
        "ai_prompt",
        "ai_file_field_id",
    ]
    serializer_field_overrides = {
        "ai_prompt": FormulaSerializerField(
            help_text="The prompt that must run for each row. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
        "ai_file_field_id": serializers.IntegerField(
            min_value=1,
            help_text="File field that will be used as a knowledge base for the AI model.",
            required=False,
            allow_null=True,
            default=None,
        ),
    }
    api_exceptions_map = {
        GenerativeAITypeDoesNotExist: ERROR_GENERATIVE_AI_DOES_NOT_EXIST,
        ModelDoesNotBelongToType: ERROR_MODEL_DOES_NOT_BELONG_TO_TYPE,
        GenerativeAITypeDoesNotSupportFileField: ERROR_GENERATIVE_AI_DOES_NOT_SUPPORT_FILE_FIELD,
        IntegrityError: ERROR_FIELD_DOES_NOT_EXIST,
    }
    can_get_unique_values = False

    def get_serializer_field(self, instance, **kwargs):
        required = kwargs.get("required", False)
        return serializers.CharField(
            **{
                "required": required,
                "allow_null": not required,
                "allow_blank": not required,
                **kwargs,
            }
        )

    def get_model_field(self, instance, **kwargs):
        return models.TextField(null=True, **kwargs)

    def get_serializer_help_text(self, instance):
        return (
            "Holds a text value that is generated by a generative AI model using a "
            "dynamic prompt."
        )

    def random_value(self, instance, fake, cache):
        return fake.name()

    def to_baserow_formula_type(self, field) -> BaserowFormulaType:
        return BaserowFormulaTextType(nullable=True)

    def from_baserow_formula_type(
        self, formula_type: BaserowFormulaTextType
    ) -> TextField:
        return TextField()

    def get_value_for_filter(self, row: "GeneratedTableModel", field: Field) -> any:
        value = getattr(row, field.db_column)
        return collate_expression(Value(value))

    def contains_query(self, *args):
        return contains_filter(*args)

    def contains_word_query(self, *args):
        return contains_word_filter(*args)

    def _validate_field_kwargs(
        self, ai_type, model_type, ai_file_field_id, workspace=None
    ):
        ai_type = generative_ai_model_type_registry.get(ai_type)
        models = ai_type.get_enabled_models(workspace=workspace)
        if model_type not in models:
            raise ModelDoesNotBelongToType(model_name=model_type)
        if ai_file_field_id is not None and not isinstance(
            ai_type, GenerativeAIWithFilesModelType
        ):
            raise GenerativeAITypeDoesNotSupportFileField()

    def before_create(
        self, table, primary, allowed_field_values, order, user, field_kwargs
    ):
        ai_type = field_kwargs.get("ai_generative_ai_type", None)
        model_type = field_kwargs.get("ai_generative_ai_model", None)
        ai_file_field_id = field_kwargs.get("ai_file_field_id", None)
        workspace = table.database.workspace
        self._validate_field_kwargs(
            ai_type, model_type, ai_file_field_id, workspace=workspace
        )

    def before_update(self, from_field, to_field_values, user, field_kwargs):
        update_field = None
        if isinstance(from_field, AIField):
            update_field = from_field

        ai_type = field_kwargs.get("ai_generative_ai_type", None) or getattr(
            update_field, "ai_generative_ai_type", None
        )
        model_type = field_kwargs.get("ai_generative_ai_model", None) or getattr(
            update_field, "ai_generative_ai_model", None
        )
        try:
            ai_file_field_id = field_kwargs["ai_file_field_id"]
        except KeyError:
            ai_file_field_id = getattr(update_field, "ai_file_field_id", None)
        workspace = from_field.table.database.workspace
        self._validate_field_kwargs(
            ai_type, model_type, ai_file_field_id, workspace=workspace
        )

    def after_import_serialized(
        self,
        field: AIField,
        field_cache,
        id_mapping,
    ):
        save = False
        if field.ai_file_field_id:
            field.ai_file_field_id = id_mapping["database_fields"][
                field.ai_file_field_id
            ]
            save = True

        if field.ai_prompt:
            try:
                field.ai_prompt = replace_field_id_references(
                    field.ai_prompt, id_mapping["database_fields"]
                )
                save = True
            except KeyError:
                # Raised when the field ID is not found in the mapping. If that's the
                # case, we leave the field ID references broken so that the import
                # can still succeed.
                pass

        if save:
            field.save()
