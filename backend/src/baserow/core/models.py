from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from baserow.core.user_files.models import UserFile

from .managers import GroupQuerySet
from .mixins import (
    OrderableMixin, PolymorphicContentTypeMixin, CreatedAndUpdatedOnMixin
)
from .exceptions import UserInvalidGroupPermissionsError


__all__ = ['UserFile']


User = get_user_model()


# The difference between an admin and member right now is that an admin rights to
# manage the members of a group.
GROUP_USER_PERMISSION_ADMIN = 'ADMIN'
GROUP_USER_PERMISSION_MEMBER = 'MEMBER'
GROUP_USER_PERMISSION_CHOICES = (
    (GROUP_USER_PERMISSION_ADMIN, 'Admin'),
    (GROUP_USER_PERMISSION_MEMBER, 'Member')
)


def get_default_application_content_type():
    return ContentType.objects.get_for_model(Application)


class Group(CreatedAndUpdatedOnMixin, models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='GroupUser')

    objects = GroupQuerySet.as_manager()

    def has_user(self, user):
        """Returns true if the user belongs to the group."""

        return self.users.filter(id=user.id).exists()

    def has_user_with_permissions(self, user, permissions):
        """
        Returns true if the user belongs to the group with the provided permissions.

        :param user: The user for which we check if it belongs to the group.
        :type user: User
        :param permissions: The permissions that the user must have.
        :type permissions: str or list
        :return: Indicates if the user belongs to the group with the right permissions.
        :rtype: bool
        """

        if not isinstance(permissions, list):
            permissions = [permissions]

        return GroupUser.objects.filter(
            user_id=user.id,
            group_id=self.id,
            permissions__in=permissions
        ).exists()

    def check_user_permissions(self, user, permissions):
        """
        Check is the provided user has the correct permissions and if not the
        appropriate exception will be raised.
        """

        if not self.has_user_with_permissions(user, permissions):
            raise UserInvalidGroupPermissionsError(user, self, permissions)

    def __str__(self):
        return f'<Group id={self.id}, name={self.name}>'


class GroupUser(CreatedAndUpdatedOnMixin, OrderableMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    permissions = models.CharField(
        default=GROUP_USER_PERMISSION_MEMBER,
        max_length=32,
        choices=GROUP_USER_PERMISSION_CHOICES
    )

    class Meta:
        ordering = ('order',)

    @classmethod
    def get_last_order(cls, user):
        queryset = cls.objects.filter(user=user)
        return cls.get_highest_order_of_queryset(queryset) + 1


class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    permissions = models.CharField(
        default=GROUP_USER_PERMISSION_MEMBER,
        max_length=32,
        choices=GROUP_USER_PERMISSION_CHOICES
    )
    message = models.TextField()


class Application(CreatedAndUpdatedOnMixin, OrderableMixin,
                  PolymorphicContentTypeMixin, models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        verbose_name='content type',
        related_name='applications',
        on_delete=models.SET(get_default_application_content_type)
    )

    class Meta:
        ordering = ('order',)

    @classmethod
    def get_last_order(cls, group):
        queryset = Application.objects.filter(group=group)
        return cls.get_highest_order_of_queryset(queryset) + 1
