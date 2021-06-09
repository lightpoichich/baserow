import pytest
from django.utils import timezone
from freezegun import freeze_time

from baserow.core.exceptions import GroupDoesNotExist
from baserow.core.models import Group
from baserow.core.trash.handler import TrashHandler
from baserow.core.models import Trash


@pytest.mark.django_db
def test_trashing_an_item_creates_a_trash_entry_in_the_db_and_marks_it_as_trashed(
    data_fixture,
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)
    assert not group_to_delete.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)
    assert group_to_delete.trashed
    trash_entry = Trash.objects.get(
        trash_item_id=group_to_delete.id, trash_item_type="group"
    )
    assert trash_entry.trashed_at.isoformat() == "2020-01-01T12:00:00+00:00"
    assert Group.objects.count() == 0
    assert Group.trash.count() == 1


@pytest.mark.django_db
def test_restoring_a_trashed_item_unmarks_it_as_trashed_and_deletes_the_entry(
    data_fixture,
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)
    TrashHandler.trash(user, group_to_delete, None, group_to_delete)
    assert group_to_delete.trashed
    assert Trash.objects.count() == 1

    TrashHandler.restore_item(user, "group", group_to_delete.id)

    group_to_delete.refresh_from_db()
    assert not group_to_delete.trashed
    assert Trash.objects.count() == 0
    assert Group.trash.count() == 0
    assert Group.objects.count() == 1


@pytest.mark.django_db
def test_a_trash_entry_older_than_setting_gets_marked_for_permanent_deletion(
    data_fixture, settings
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)

    trashed_at = timezone.now()
    half_time = timezone.timedelta(
        hours=settings.HOUR_DURATION_UNTIL_TRASH_ITEM_PERMANENTLY_DELETED / 2
    )
    plus_one_hour_over = timezone.timedelta(
        hours=settings.HOUR_DURATION_UNTIL_TRASH_ITEM_PERMANENTLY_DELETED + 1
    )
    with freeze_time(trashed_at):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)

    entry = TrashHandler.get_trash_entry(user, "group", group_to_delete.id)
    assert not entry.should_be_permanently_deleted

    datetime_when_trash_item_should_still_be_kept = trashed_at + half_time
    with freeze_time(datetime_when_trash_item_should_still_be_kept):
        TrashHandler.mark_old_trash_for_permanent_deletion()

    entry.refresh_from_db()
    assert not entry.should_be_permanently_deleted

    datetime_when_trash_item_old_enough_to_be_deleted = trashed_at + plus_one_hour_over
    with freeze_time(datetime_when_trash_item_old_enough_to_be_deleted):
        TrashHandler.mark_old_trash_for_permanent_deletion()

    entry.refresh_from_db()
    assert entry.should_be_permanently_deleted


@pytest.mark.django_db
def test_a_trash_entry_marked_for_permanent_deletion_gets_deleted_by_task(
    data_fixture, settings
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)

    trashed_at = timezone.now()
    plus_one_hour_over = timezone.timedelta(
        hours=settings.HOUR_DURATION_UNTIL_TRASH_ITEM_PERMANENTLY_DELETED + 1
    )
    with freeze_time(trashed_at):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)

    TrashHandler.permanently_delete_marked_trash()
    assert Group.trash.count() == 1

    datetime_when_trash_item_old_enough_to_be_deleted = trashed_at + plus_one_hour_over
    with freeze_time(datetime_when_trash_item_old_enough_to_be_deleted):
        TrashHandler.mark_old_trash_for_permanent_deletion()

    TrashHandler.permanently_delete_marked_trash()
    assert Group.objects.count() == 0


@pytest.mark.django_db
def test_a_group_marked_for_perm_deletion_raises_a_404_when_asked_for_trash_contents(
    data_fixture,
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)
    assert not group_to_delete.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)
    trash_entry = Trash.objects.get(
        trash_item_id=group_to_delete.id, trash_item_type="group"
    )
    trash_entry.should_be_permanently_deleted = True
    trash_entry.save()

    with pytest.raises(GroupDoesNotExist):
        TrashHandler.get_trash_contents(user, group_to_delete.id, None)


@pytest.mark.django_db
def test_a_group_marked_for_perm_deletion_no_longer_shows_up_in_trash_structure(
    data_fixture,
):
    user = data_fixture.create_user()
    group_to_delete = data_fixture.create_group(user=user)
    assert not group_to_delete.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)
    trash_entry = Trash.objects.get(
        trash_item_id=group_to_delete.id, trash_item_type="group"
    )
    trash_entry.should_be_permanently_deleted = True
    trash_entry.save()

    assert TrashHandler.get_trash_structure(user)["groups"].count() == 0
