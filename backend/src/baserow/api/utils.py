from contextlib import contextmanager

from django.utils.encoding import force_text

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request

from baserow.core.exceptions import InstanceTypeDoesNotExist

from .exceptions import RequestBodyValidationException


@contextmanager
def map_exceptions(mapping):
    """
    This utility function simplifies mapping uncaught exceptions to a standard api
    response exception.

    Example:
      with map_api_exceptions({ SomeException: 'ERROR_1' }):
          raise SomeException('This is a test')

      HTTP/1.1 400
      {
        "error": "ERROR_1",
        "detail": "This is a test"
      }

    Example 2:
      with map_api_exceptions({ SomeException: ('ERROR_1', 404, 'Other message') }):
          raise SomeException('This is a test')

      HTTP/1.1 404
      {
        "error": "ERROR_1",
        "detail": "Other message"
      }
    """

    try:
        yield
    except tuple(mapping.keys()) as e:
        value = mapping.get(e.__class__)
        status_code = status.HTTP_400_BAD_REQUEST
        detail = ""

        if isinstance(value, str):
            error = value
        if isinstance(value, tuple):
            error = value[0]
            if len(value) > 1 and value[1] is not None:
                status_code = value[1]
            if len(value) > 2 and value[2] is not None:
                detail = value[2].format(e=e)

        exc = APIException({"error": error, "detail": detail})
        exc.status_code = status_code

        raise exc


def validate_data(serializer_class, data):
    """
    Validates the provided data via the provided serializer class. If the data doesn't
    match with the schema of the serializer an api exception containing more detailed
    information will be raised.

    :param serializer_class: The serializer that must be used for validating.
    :type serializer_class: Serializer
    :param data: The data that needs to be validated.
    :type data: dict
    :return: The data after being validated by the serializer.
    :rtype: dict
    """

    def serialize_errors_recursive(error):
        if isinstance(error, dict):
            return {
                key: serialize_errors_recursive(errors) for key, errors in error.items()
            }
        elif isinstance(error, list):
            return [serialize_errors_recursive(errors) for errors in error]
        else:
            return {"error": force_text(error), "code": error.code}

    serializer = serializer_class(data=data)
    if not serializer.is_valid():
        detail = serialize_errors_recursive(serializer.errors)
        raise RequestBodyValidationException(detail)

    return serializer.data


def validate_data_custom_fields(
    type_name, registry, data, base_serializer_class=None, type_attribute_name="type"
):
    """
    Validates the provided data with the serializer generated by the registry based on
    the provided type_name and provided base_serializer_class.

    :param type_name: The type name of the type instance that is needed to generated
        the serializer.
    :type type_name: str
    :param registry: The registry where to get the type instance from.
    :type registry: Registry
    :param data: The data that needs to be validated.
    :type data: dict
    :param base_serializer_class: The base serializer class that is used when
        generating the serializer for validation.
    :type base_serializer_class: ModelSerializer
    :param type_attribute_name: The attribute key name that contains the type value.
    :type type_attribute_name: str
    :raises RequestBodyValidationException: When the type is not a valid choice.
    :return: The validated data.
    :rtype: dict
    """

    try:
        type_instance = registry.get(type_name)
    except InstanceTypeDoesNotExist:
        # If the provided type name doesn't exist we will raise a machine
        # readable validation error.
        raise RequestBodyValidationException(
            {
                type_attribute_name: [
                    {
                        "error": f'"{type_name}" is not a valid choice.',
                        "code": "invalid_choice",
                    }
                ]
            }
        )

    serializer_kwargs = {"base_class": base_serializer_class}
    serializer_class = type_instance.get_serializer_class(**serializer_kwargs)
    return validate_data(serializer_class, data)


def get_request(args):
    """
    A small helper function that checks if the request is in the args and returns that
    request.

    :param args: A list containing the original arguments of the called view method.
    :type args: list
    :raises ValueError: When the request has not been found in the args.
    :return: The extracted request object.
    :rtype: Request
    """

    if len(args) < 2 or not isinstance(args[1], Request):
        raise ValueError("There must be a request in the args.")

    return args[1]


def type_from_data_or_registry(
    data, registry, model_instance, type_attribute_name="type"
):
    """
    Returns the type in the provided data else the type will be returned via the
    registry.

    :param data: The data that might contains the type name.
    :type data: dict
    :param registry: The registry where to get the type instance from if not provided in
        the data.
    :type registry: Registry
    :param model_instance: The model instance we want to know the type from if not
        provided in the data.
    :type model_instance: Model
    :param type_attribute_name: The expected type attribute name in the data.
    :type type_attribute_name: str
    :return: The extracted type.
    :rtype: str
    """

    if type_attribute_name in data:
        return data[type_attribute_name]
    else:
        return registry.get_by_model(model_instance.specific_class).type


def get_serializer_class(model, field_names, field_overrides=None, base_class=None):
    """
    Generates a model serializer based on the provided field names and field overrides.

    :param model: The model class that must be used for the ModelSerializer.
    :type model: Model
    :param field_names: The model field names that must be added to the serializer.
    :type field_names: list
    :param field_overrides: A dict containing field overrides where the key is the name
        and the value must be a serializer Field.
    :type field_overrides: dict
    :param base_class: The class that must be extended.
    :type base_class: ModelSerializer
    :return: The generated model serializer containing the provided fields.
    :rtype: ModelSerializer
    """

    model_ = model
    meta_ref_name = model_.__name__

    if not field_overrides:
        field_overrides = {}

    if base_class:
        meta_ref_name += base_class.__name__

    if not base_class:
        base_class = ModelSerializer

    extends_meta = object

    if hasattr(base_class, "Meta"):
        extends_meta = getattr(base_class, "Meta")
        field_names = list(extends_meta.fields) + list(field_names)

    class Meta(extends_meta):
        ref_name = meta_ref_name
        model = model_
        fields = list(field_names)

    attrs = {"Meta": Meta}

    if field_overrides:
        attrs.update(field_overrides)

    return type(str(model_.__name__ + "Serializer"), (base_class,), attrs)


class PolymorphicCustomFieldRegistrySerializer:
    """
    A placeholder class for the `PolymorphicCustomFieldRegistrySerializerExtension`
    extension class.
    """

    def __init__(self, registry, base_class, type_field_name="type", many=False):
        self.read_only = False
        self.registry = registry
        self.base_class = base_class
        self.type_field_name = type_field_name
        self.many = many


class PolymorphicMappingSerializer:
    """
    A placeholder class for the `PolymorphicMappingSerializerExtension` extension class.
    """

    def __init__(self, component_name, mapping, type_field_name="type", many=False):
        self.read_only = False
        self.component_name = component_name
        self.mapping = mapping
        self.type_field_name = type_field_name
        self.many = many
