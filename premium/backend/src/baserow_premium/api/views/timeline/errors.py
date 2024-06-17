from rest_framework.status import HTTP_400_BAD_REQUEST

ERROR_TIMELINE_VIEW_HAS_NO_START_DATE_FIELD = (
    "ERROR_TIMELINE_VIEW_HAS_NO_START_DATE_FIELD",
    HTTP_400_BAD_REQUEST,
    "The requested timeline view does not have a start date field.",
)

ERROR_TIMELINE_VIEW_HAS_NO_END_DATE_FIELD = (
    "ERROR_TIMELINE_VIEW_HAS_NO_END_DATE_FIELD",
    HTTP_400_BAD_REQUEST,
    "The requested timeline view does not have an end date field.",
)
