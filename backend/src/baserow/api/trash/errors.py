from rest_framework.status import HTTP_400_BAD_REQUEST


ERROR_CANNOT_RESTORE_PARENT_BEFORE_CHILD = (
    "ERROR_CANNOT_RESTORE_PARENT_BEFORE_CHILD",
    HTTP_400_BAD_REQUEST,
    "Cannot restore a trashed item if it's parent is also trashed, please restore the "
    "parent first.",
)
