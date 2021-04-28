from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

ERROR_ADMIN_ONLY_OPERATION = (
    "ERROR_ADMIN_ONLY_OPERATION",
    HTTP_401_UNAUTHORIZED,
    "You do not have permission to perform this operation.",
)

INVALID_SORT_DIRECTION = (
    "INVALID_SORT_DIRECTION",
    HTTP_400_BAD_REQUEST,
    "Attributes to sort by must be prefixed with one of '-' or '+'.",
)

INVALID_SORT_ATTRIBUTE = (
    "INVALID_SORT_ATTRIBUTE",
    HTTP_400_BAD_REQUEST,
    "Invalid attribute name provided to sort by.",
)


class InvalidSortDirectionException(Exception):
    """
    Raised when an invalid sort direction is provided.
    """
