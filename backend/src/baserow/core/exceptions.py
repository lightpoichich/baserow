class UserNotInGroupError(Exception):
    """Raised when the user doesn't have access to the related group."""

    def __init__(self, user=None, group=None, *args, **kwargs):
        if user and group:
            super().__init__(f'User {user} doesn\'t belong to group {group}.', *args,
                             **kwargs)
        else:
            super().__init__('The user doesn\'t belong to the group', *args, **kwargs)


class UserInvalidGroupPermissionsError(Exception):
    """Raised when a user doesn't have the right permissions for the related group."""

    def __init__(self, user, group, permissions, *args, **kwargs):
        self.user = user
        self.group = group
        self.permissions = permissions
        super().__init__(
            f'The user {user} doesn\'t have the right permissions {permissions} to '
            f'{group}.',
            *args,
            **kwargs
        )


class GroupDoesNotExist(Exception):
    """Raised when trying to get a group that does not exist."""


class ApplicationDoesNotExist(Exception):
    """Raised when trying to get an application that does not exist."""


class InstanceTypeAlreadyRegistered(Exception):
    """
    Raised when the instance model instance is already registered in the registry.
    """


class InstanceTypeDoesNotExist(Exception):
    """
    Raised when a requested instance model instance isn't registered in the registry.
    """

    def __init__(self, type_name, *args, **kwargs):
        self.type_name = type_name
        super().__init__(*args, **kwargs)


class ApplicationTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class ApplicationTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class BaseURLHostnameNotAllowed(Exception):
    """
    Raised when the provided base url is not allowed when requesting a password
    reset email.
    """


class GroupInvitationDoesNotExist(Exception):
    """
    Raised when the requested group invitation doesn't exist.
    """


class GroupInvitationEmailMismatch(Exception):
    """
    Raised when the group invitation email is not the expected email address.
    """
