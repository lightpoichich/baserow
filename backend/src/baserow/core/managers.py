from django.db import models


class ParentNonTrashedManager(models.Manager):
    """ Query only objects which do not have a trashed parent object. """

    def get_queryset(self):
        return super().get_queryset().filter(**{f"{self.parent}__trashed": False})


class ParentTrashedManager(models.Manager):
    """ Query only objects which do have a trashed parent object. """

    def get_queryset(self):
        return super().get_queryset().filter(**{f"{self.parent}__trashed": True})


class NonTrashedManager(models.Manager):
    """ Query only objects which have not been trashed. """

    def get_queryset(self):
        return super().get_queryset().filter(trashed=False)


class TrashedManager(models.Manager):
    """ Query only objects which have been trashed. """

    def get_queryset(self):
        return super().get_queryset().filter(trashed=True)


class GroupParentNonTrashedManager(ParentNonTrashedManager):
    parent = "group"


class GroupParentTrashedManager(ParentTrashedManager):
    parent = "group"
