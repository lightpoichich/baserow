from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


ERROR_ROW_DOES_NOT_EXIST = (
    "ERROR_ROW_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The requested row does not exist.",
)

ERROR_KEY_NOT_FOUND = (
    "ERROR_KEY_NOT_FOUND",
    HTTP_400_BAD_REQUEST,
    "Foreign key constraint violation",
)
