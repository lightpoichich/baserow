class AdminOnlyOperationException(Exception):
    """
    Raised when a non-admin user attempts to perform an operation which is admin only.
    """


class CannotDeactivateYourselfException(Exception):
    """
    Raised when an admin user attempts to deactivate or unstaff themself.
    """


class CannotDeleteYourselfException(Exception):
    """
    Raised when an admin user attempts to delete themself.
    """
