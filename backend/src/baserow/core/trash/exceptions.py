class CannotRestoreChildBeforeParent(Exception):
    """
    Raised when attempting to restore a trashed item when it's parent is also trashed.
    """
