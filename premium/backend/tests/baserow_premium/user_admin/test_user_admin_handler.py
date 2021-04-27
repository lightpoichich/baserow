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
