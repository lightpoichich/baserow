class AdminOnlyOperationException(Exception):
    """
    Raised when a non-admin user attempts to perform an operation which is admin only.
    """
