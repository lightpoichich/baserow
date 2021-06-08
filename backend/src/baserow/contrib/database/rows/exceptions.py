class RowDoesNotExist(Exception):
    """Raised when trying to get a row that doesn't exist."""


class KeyNotFound(Exception):
    """Raised when trying to set a linked row field to a non-existent entity"""
