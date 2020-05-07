from baserow.core.exceptions import (
    InstanceTypeDoesNotExist, InstanceTypeAlreadyRegistered
)


class ViewDoesNotExist(Exception):
    """Raised when trying to get a view that doesn't exist."""


class UnrelatedFieldError(Exception):
    """
    Raised when a field is not related to the view. For example when unrelated field
    options are being updated.
    """


class ViewTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class ViewTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass
