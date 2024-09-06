class PropertyNotFound(Exception):
    """Raised when the property is not found in the data sync."""


class UniquePrimaryPropertyNotFound(Exception):
    """
    Raised when the data sync didn't return a property with `unique_primary=True`. At
    least one is required.
    """
