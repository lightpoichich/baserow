from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


ERROR_ROW_DOES_NOT_EXIST = (
    "ERROR_ROW_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The requested row does not exist.",
)

ERROR_DUPLICATE_KEY = (
    "ERROR_ROW_DUPLICATE_KEY",
    HTTP_409_CONFLICT,
    "The requested update violates a unique key constraint",
)
