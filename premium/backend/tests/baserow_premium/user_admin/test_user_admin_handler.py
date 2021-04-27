import pytest
from django.contrib.auth import get_user_model

from baserow_premium.user_admin.exceptions import AdminOnlyOperationException
from baserow_premium.user_admin.handler import UserAdminHandler

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
            "id": user_to_modify.id,
            "username": "new_email@example.com",
            "full_name": "new full name",
            "is_staff": True,
            "is_active": True,
            "password": "new_password",
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
def test_unknown_fields_when_updating_a_user_will_be_ignored(data_fixture):
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
    updated_user = handler.update_user(
        admin_user,
        user_to_modify.id,
        {
            "id": user_to_modify.id,
            "username": "new_email@example.com",
            "some_unknown_field": "blah",
        },
    )
    assert updated_user.username == "new_email@example.com"
    assert updated_user.email == "new_email@example.com"
    assert not hasattr(updated_user, "some_unknown_field")


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
            "id": user_to_modify.id,
            "password": "new_password",
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
            {"id": non_admin_user.id, "username": "new_email@example.com"},
        )
    non_admin_user.refresh_from_db()
    assert non_admin_user.username == "test@test.nl"
