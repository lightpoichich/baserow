import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.datetime_safe import datetime

from baserow_premium.user_admin.exceptions import (
    AdminOnlyOperationException,
    CannotDeactivateYourselfException,
    CannotDeleteYourselfException,
    UnknownUserException,
)
from baserow_premium.user_admin.handler import (
    UserAdminHandler,
    EditableUserAdminField,
    UserAdminSort,
    SortableUserAdminField,
    UserAdminSortDirection,
)

User = get_user_model()


@pytest.mark.django_db
def test_admin_can_get_users(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    assert handler.get_users(admin_user).count() == 1


@pytest.mark.django_db
def test_non_admin_cant_get_users(data_fixture):
    handler = UserAdminHandler()
    non_admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
    )
    with pytest.raises(AdminOnlyOperationException):
        handler.get_users(non_admin_user)


@pytest.mark.django_db
def test_admin_can_search_by_username(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    data_fixture.create_user(
        email="other_user@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    results = handler.get_users(admin_user, username_search="other_user")
    assert results.count() == 1
    assert results[0].username == "other_user@test.nl"


@pytest.mark.django_db
def test_admin_can_sort_by_multiple_fields_in_specified_order_and_directions(
    data_fixture,
):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=False,
        date_joined=datetime(2020, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    data_fixture.create_user(
        email="other_user1@test.nl",
        password="password",
        first_name="Test2",
        is_staff=True,
        is_active=True,
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    data_fixture.create_user(
        email="other_user2@test.nl",
        password="password",
        first_name="Test3",
        is_staff=True,
        is_active=True,
        date_joined=datetime(2022, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    results = handler.get_users(
        admin_user,
        sorts=[
            UserAdminSort(UserAdminSortDirection.ASC, SortableUserAdminField.IS_ACTIVE),
            UserAdminSort(
                UserAdminSortDirection.DESC, SortableUserAdminField.DATE_JOINED
            ),
        ],
    )
    assert results.count() == 3
    assert results[0].first_name == "Test2"
    assert results[1].first_name == "Test3"
    assert results[2].first_name == "Test1"


@pytest.mark.django_db
def test_admin_can_delete_user(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    user_to_delete = data_fixture.create_user(
        email="delete_me@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    handler.delete_user(admin_user, user_to_delete.id)
    assert not User.objects.filter(id=user_to_delete.id).exists()


@pytest.mark.django_db
def test_non_admin_cant_delete_user(data_fixture):
    handler = UserAdminHandler()
    non_admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
    )
    with pytest.raises(AdminOnlyOperationException):
        handler.delete_user(non_admin_user, non_admin_user.id)


@pytest.mark.django_db
def test_admin_can_modify_allowed_user_attributes(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    user_to_modify = data_fixture.create_user(
        email="delete_me@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
        is_active=False,
    )
    old_password = user_to_modify.password
    handler.update_user(
        admin_user,
        user_to_modify.id,
        {
            EditableUserAdminField.USERNAME: "new_email@example.com",
            EditableUserAdminField.FULL_NAME: "new full name",
            EditableUserAdminField.IS_ACTIVE: True,
            EditableUserAdminField.IS_STAFF: True,
            EditableUserAdminField.PASSWORD: "new_password",
        },
    )
    user_to_modify.refresh_from_db()
    assert user_to_modify.username == "new_email@example.com"
    assert user_to_modify.email == "new_email@example.com"
    assert user_to_modify.first_name == "new full name"
    assert user_to_modify.is_staff
    assert user_to_modify.is_active
    assert old_password != user_to_modify.password


@pytest.mark.django_db
def test_updating_a_users_password_uses_djangos_built_in_smart_set_password(
    data_fixture, mocker
):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    user_to_modify = data_fixture.create_user(
        email="delete_me@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
        is_active=False,
    )
    old_password_hash = user_to_modify.password
    set_password_spy = mocker.spy(User, "set_password")
    updated_user = handler.update_user(
        admin_user,
        user_to_modify.id,
        {
            EditableUserAdminField.PASSWORD: "new_password",
        },
    )
    assert updated_user.password != "new_password"
    assert updated_user.password != old_password_hash
    assert set_password_spy.call_count == 1


@pytest.mark.django_db
def test_non_admin_cant_edit_user(data_fixture):
    handler = UserAdminHandler()
    non_admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
    )
    with pytest.raises(AdminOnlyOperationException):
        handler.update_user(
            non_admin_user,
            non_admin_user.id,
            {EditableUserAdminField.USERNAME: "new_email@example.com"},
        )
    non_admin_user.refresh_from_db()
    assert non_admin_user.username == "test@test.nl"


@pytest.mark.django_db
def test_admin_cant_deactivate_themselves(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=True,
    )
    with pytest.raises(CannotDeactivateYourselfException):
        handler.update_user(
            admin_user,
            admin_user.id,
            {EditableUserAdminField.IS_ACTIVE: False},
        )
    admin_user.refresh_from_db()
    assert admin_user.is_active


@pytest.mark.django_db
def test_admin_cant_destaff_themselves(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=True,
    )
    with pytest.raises(CannotDeactivateYourselfException):
        handler.update_user(
            admin_user,
            admin_user.id,
            {EditableUserAdminField.IS_STAFF: False},
        )
    admin_user.refresh_from_db()
    assert admin_user.is_staff


@pytest.mark.django_db
def test_admin_cant_delete_themselves(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=True,
    )
    with pytest.raises(CannotDeleteYourselfException):
        handler.delete_user(admin_user, admin_user.id)

    assert User.objects.filter(id=admin_user.id).exists()


@pytest.mark.django_db
def test_raises_exception_when_deleting_an_unknown_user(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=True,
    )
    with pytest.raises(UnknownUserException):
        handler.delete_user(admin_user, 99999)


@pytest.mark.django_db
def test_raises_exception_when_updating_an_unknown_user(data_fixture):
    handler = UserAdminHandler()
    admin_user = data_fixture.create_user(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        is_active=True,
    )
    with pytest.raises(UnknownUserException):
        handler.update_user(
            admin_user, 99999, {EditableUserAdminField.USERNAME: "new_password"}
        )
