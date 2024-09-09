class PropertyNotFound(Exception):
    """Raised when the property is not found in the data sync."""


class UniquePrimaryPropertyNotFound(Exception):
    """
    Raised when the data sync didn't return a property with `unique_primary=True`. At
    least one is required.
    """


class SyncError(Exception):
    """
    This exception can be raised when something goes wrong during the data sync,
    and it doesn't have to fail hard. The provided error will be stored in the
    database, exposed via the API, and readable to the user. It should always be in
    English.
    """
