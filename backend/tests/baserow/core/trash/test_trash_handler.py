import pytest
from django.utils import timezone
from freezegun import freeze_time

from baserow.contrib.database.rows.handler import RowHandler
from baserow.core.exceptions import GroupDoesNotExist, ApplicationDoesNotExist
from baserow.core.models import Group, Application
from baserow.core.models import Trash
from baserow.core.trash.exceptions import CannotRestoreChildBeforeParent
from baserow.core.trash.handler import TrashHandler


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

    TrashHandler.restore_item(user, "group", None, group_to_delete.id)

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
        hours=settings.HOURS_UNTIL_TRASH_PERMANENTLY_DELETED / 2
    )
    plus_one_hour_over = timezone.timedelta(
        hours=settings.HOURS_UNTIL_TRASH_PERMANENTLY_DELETED + 1
    )
    with freeze_time(trashed_at):
        TrashHandler.trash(user, group_to_delete, None, group_to_delete)

    entry = TrashHandler.get_trash_entry(user, "group", None, group_to_delete.id)
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
        hours=settings.HOURS_UNTIL_TRASH_PERMANENTLY_DELETED + 1
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

    assert len(TrashHandler.get_trash_structure(user)["groups"]) == 0


@pytest.mark.django_db
def test_an_app_marked_for_perm_deletion_raises_a_404_when_asked_for_trash_contents(
    data_fixture,
):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    trashed_database = data_fixture.create_database_application(user=user, group=group)
    assert not trashed_database.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group, trashed_database, trashed_database)
    trash_entry = Trash.objects.get(
        trash_item_id=trashed_database.id, trash_item_type="application"
    )
    trash_entry.should_be_permanently_deleted = True
    trash_entry.save()

    with pytest.raises(ApplicationDoesNotExist):
        TrashHandler.get_trash_contents(user, group.id, trashed_database.id)


@pytest.mark.django_db
def test_a_trashed_app_shows_up_in_trash_structure(
    data_fixture,
):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    trashed_database = data_fixture.create_database_application(user=user, group=group)
    assert not trashed_database.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group, trashed_database, trashed_database)

    structure = TrashHandler.get_trash_structure(user)
    applications_qs = structure["groups"][0]["applications"]
    assert applications_qs.count() == 1
    assert applications_qs.get().trashed


@pytest.mark.django_db
def test_an_app_marked_for_perm_deletion_no_longer_shows_up_in_trash_structure(
    data_fixture,
):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    trashed_database = data_fixture.create_database_application(user=user, group=group)
    assert not trashed_database.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group, trashed_database, trashed_database)
    trash_entry = Trash.objects.get(
        trash_item_id=trashed_database.id, trash_item_type="application"
    )
    trash_entry.should_be_permanently_deleted = True
    trash_entry.save()

    for group in TrashHandler.get_trash_structure(user)["groups"]:
        assert group["applications"].count() == 0


@pytest.mark.django_db
def test_perm_deleting_a_parent_with_a_trashed_child_also_cleans_up_the_child_entry(
    data_fixture,
):
    # TODO Trash: Add case for table and row!
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    trashed_database = data_fixture.create_database_application(user=user, group=group)
    assert not trashed_database.trashed
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group, trashed_database, trashed_database)
        TrashHandler.trash(user, group, None, group)
    parent_trash_entry = Trash.objects.get(
        trash_item_id=group.id, trash_item_type="group"
    )
    parent_trash_entry.should_be_permanently_deleted = True
    parent_trash_entry.save()

    assert Trash.objects.count() == 2

    TrashHandler.permanently_delete_marked_trash()

    assert Trash.objects.count() == 0
    assert Group.objects_and_trash.count() == 0
    assert Application.objects_and_trash.count() == 0


@pytest.mark.django_db
def test_trash_contents_are_ordered_from_newest_to_oldest_entries(
    data_fixture,
):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    trashed_database = data_fixture.create_database_application(user=user, group=group)

    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, group, trashed_database, trashed_database)
    with freeze_time("2020-01-01 12:02"):
        TrashHandler.trash(user, group, None, group)

    contents = TrashHandler.get_trash_contents(user, group.id, None)

    assert contents[0].trash_item_type == "group"
    assert contents[0].trash_item_id == group.id
    assert contents[0].trashed_at.isoformat() == "2020-01-01T12:02:00+00:00"

    assert contents[1].trash_item_type == "application"
    assert contents[1].trash_item_id == trashed_database.id
    assert contents[1].trashed_at.isoformat() == "2020-01-01T12:00:00+00:00"


@pytest.mark.django_db
def test_perm_deleting_one_group_should_not_effect_another_trashed_group(
    data_fixture,
):
    user = data_fixture.create_user()
    trashed_group = data_fixture.create_group(user=user)
    other_trashed_group = data_fixture.create_group(user=user)
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, trashed_group, None, trashed_group)
        TrashHandler.trash(user, other_trashed_group, None, other_trashed_group)

    # Only mark one for deletion
    parent_trash_entry = Trash.objects.get(
        trash_item_id=trashed_group.id, trash_item_type="group"
    )
    parent_trash_entry.should_be_permanently_deleted = True
    parent_trash_entry.save()

    assert Trash.objects.count() == 2
    assert Trash.objects.filter(should_be_permanently_deleted=True).count() == 1
    assert Group.objects_and_trash.count() == 2

    TrashHandler.permanently_delete_marked_trash()

    assert Trash.objects.count() == 1
    assert Group.objects_and_trash.count() == 1


@pytest.mark.django_db
def test_deleting_a_user_who_trashed_items_should_still_leave_those_items_trashed(
    data_fixture,
):
    user = data_fixture.create_user()
    trashed_group = data_fixture.create_group(user=user)
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(user, trashed_group, None, trashed_group)

    assert Trash.objects.count() == 1
    assert Group.objects_and_trash.count() == 1

    user.delete()

    assert Trash.objects.count() == 1
    assert Group.objects_and_trash.count() == 1


@pytest.mark.django_db
def test_trashing_two_rows_in_different_tables_works_as_expected(
    data_fixture,
):
    user = data_fixture.create_user()
    table_1 = data_fixture.create_database_table(name="Car", user=user)
    table_2 = data_fixture.create_database_table(name="Other Cars", user=user)
    group = data_fixture.create_group(user=user)
    name_field = data_fixture.create_text_field(
        table=table_1, name="Name", text_default="Test"
    )

    handler = RowHandler()

    row_in_table_1 = handler.create_row(
        user=user,
        table=table_1,
        values={
            name_field.id: "Tesla",
        },
    )
    row_in_table_2 = handler.create_row(
        user=user,
        table=table_2,
        values={
            name_field.id: "Ford",
        },
    )
    with freeze_time("2020-01-01 12:00"):
        TrashHandler.trash(
            user, group, table_1.database, row_in_table_1, parent_id=table_1.id
        )
        TrashHandler.trash(
            user, group, table_2.database, row_in_table_2, parent_id=table_2.id
        )

    table_1_model = table_1.get_model()
    table_2_model = table_2.get_model()

    assert table_1_model.trash.count() == 1
    assert table_1_model.objects.count() == 0

    assert table_2_model.trash.count() == 1
    assert table_2_model.objects.count() == 0

    TrashHandler.restore_item(user, "row", table_1.id, row_in_table_1.id)

    assert table_1_model.trash.count() == 0
    assert table_1_model.objects.count() == 1

    assert table_2_model.trash.count() == 1
    assert table_2_model.objects.count() == 0


@pytest.mark.django_db
def test_cannot_restore_a_child_before_the_parent(
    data_fixture,
):
    user = data_fixture.create_user()
    table_1 = data_fixture.create_database_table(name="Car", user=user)
    group = table_1.database.group
    name_field = data_fixture.create_text_field(
        table=table_1, name="Name", text_default="Test"
    )

    handler = RowHandler()

    row_in_table_1 = handler.create_row(
        user=user,
        table=table_1,
        values={
            name_field.id: "Tesla",
        },
    )
    TrashHandler.trash(
        user, group, table_1.database, row_in_table_1, parent_id=table_1.id
    )
    TrashHandler.trash(user, group, table_1.database, table_1)

    with pytest.raises(CannotRestoreChildBeforeParent):
        TrashHandler.restore_item(user, "row", table_1.id, row_in_table_1.id)

    TrashHandler.trash(user, group, table_1.database, table_1.database)
    TrashHandler.trash(user, group, None, group)

    with pytest.raises(CannotRestoreChildBeforeParent):
        TrashHandler.restore_item(user, "application", group.id, table_1.database.id)

    TrashHandler.restore_item(user, "group", None, group.id)

    with pytest.raises(CannotRestoreChildBeforeParent):
        TrashHandler.restore_item(user, "table", table_1.database.id, table_1.id)
