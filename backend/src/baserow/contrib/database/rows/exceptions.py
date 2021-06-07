class RowDoesNotExist(Exception):
    """Raised when trying to get a row that doesn't exist."""


class DuplicateKey(Exception):
    """Raised when trying to store a duplicate value in a column marked as unique"""
