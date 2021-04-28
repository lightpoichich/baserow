class AdminOnlyOperationException(Exception):
    """
    Raised when a non-admin user attempts to perform an operation which is admin only.
    """


class InvalidSortAttributeException(Exception):
    """
    Raised when a sort is requested for an invalid or non-existent field.
    """
