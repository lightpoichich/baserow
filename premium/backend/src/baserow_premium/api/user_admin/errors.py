from rest_framework.status import HTTP_401_UNAUTHORIZED

ERROR_ADMIN_ONLY_OPERATION = (
    "ERROR_ADMIN_ONLY_OPERATION",
    HTTP_401_UNAUTHORIZED,
    "You do not have permission to perform this operation.",
)
