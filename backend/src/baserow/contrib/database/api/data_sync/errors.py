from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

ERROR_PROPERTY_NOT_FOUND = (
    "ERROR_PROPERTY_NOT_FOUND",
    HTTP_400_BAD_REQUEST,
    "The property {e.property} is not found for the data sync type.",
)
ERROR_DATA_SYNC_DOES_NOT_EXIST = (
    "ERROR_DATA_SYNC_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The provided data sync or table does not exist.",
)
