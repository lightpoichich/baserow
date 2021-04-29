from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

ERROR_ADMIN_ONLY_OPERATION = (
    "ERROR_ADMIN_ONLY_OPERATION",
    HTTP_401_UNAUTHORIZED,
    "You do not have permission to perform this operation.",
)
INVALID_USER_ADMIN_UPDATE = (
    "INVALID_USER_ADMIN_UPDATE",
    HTTP_400_BAD_REQUEST,
    "An invalid or un-editable field was provided to update.",
)

INVALID_USER_ADMIN_SORT_DIRECTION = (
    "INVALID_USER_ADMIN_SORT_DIRECTION",
    HTTP_400_BAD_REQUEST,
    "Attributes to sort by must be prefixed with one of '-' or '+'.",
)

INVALID_USER_ADMIN_SORT_ATTRIBUTE = (
    "INVALID_USER_ADMIN_SORT_ATTRIBUTE",
    HTTP_400_BAD_REQUEST,
    "Invalid attribute name provided to sort by.",
)


class InvalidSortDirectionException(Exception):
    """
    Raised when an invalid sort direction is provided.
    """


class InvalidSortAttributeException(Exception):
    """
    Raised when a sort is requested for an invalid or non-existent field.
    """


class InvalidUserAdminEditField(Exception):
    """
    Raised when an edit is attempted on a invalid or un-editable user admin field.
    """
