from rest_framework.status import HTTP_400_BAD_REQUEST

ERROR_PROPERTY_NOT_FOUND = (
    "ERROR_PROPERTY_NOT_FOUND",
    HTTP_400_BAD_REQUEST,
    "The property {e.property} is not found for the data sync type.",
)
