from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

ERROR_ADMIN_ONLY_OPERATION = (
    "ERROR_ADMIN_ONLY_OPERATION",
    HTTP_401_UNAUTHORIZED,
    "You do not have permission to perform this operation.",
)

USER_ADMIN_INVALID_UPDATE_ATTRIBUTE = (
    "USER_ADMIN_INVALID_UPDATE_ATTRIBUTE",
    HTTP_400_BAD_REQUEST,
    "An invalid or un-editable field was provided to update.",
)

USER_ADMIN_INVALID_SORT_DIRECTION = (
    "USER_ADMIN_INVALID_SORT_DIRECTION",
    HTTP_400_BAD_REQUEST,
    "Attributes to sort by must be prefixed with one of '-' or '+'.",
)

USER_ADMIN_INVALID_SORT_ATTRIBUTE = (
    "USER_ADMIN_INVALID_SORT_ATTRIBUTE",
    HTTP_400_BAD_REQUEST,
    "Invalid attribute name provided to sort by.",
)

USER_ADMIN_CANNOT_DEACTIVATE_SELF = (
    "USER_ADMIN_CANNOT_DEACTIVATE_SELF",
    HTTP_400_BAD_REQUEST,
    "You cannot de-activate or un-staff yourself.",
)

USER_ADMIN_CANNOT_DELETE_SELF = (
    "USER_ADMIN_CANNOT_DELETE_SELF",
    HTTP_400_BAD_REQUEST,
    "You cannot delete yourself.",
)

USER_ADMIN_UNKNOWN_USER = (
    "USER_ADMIN_UNKNOWN_USER",
    HTTP_400_BAD_REQUEST,
    "Unknown user supplied.",
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
