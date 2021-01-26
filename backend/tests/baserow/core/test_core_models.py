import pytest
from pytz import timezone
from freezegun import freeze_time
from datetime import datetime

from baserow.core.models import GroupUser, Group
from baserow.core.exceptions import UserInvalidGroupPermissionsError
from baserow.contrib.database.models import Database


@pytest.mark.django_db
def test_created_and_updated_on_mixin():
    with freeze_time('2020-01-01 12:00'):
        group = Group.objects.create(name='Group')

    assert group.created_on == datetime(2020, 1, 1, 12, 00, tzinfo=timezone('UTC'))
    assert group.updated_on == datetime(2020, 1, 1, 12, 00, tzinfo=timezone('UTC'))

    with freeze_time('2020-01-02 12:00'):
        group.name = 'Group2'
        group.save()

    assert group.created_on == datetime(2020, 1, 1, 12, 00, tzinfo=timezone('UTC'))
    assert group.updated_on == datetime(2020, 1, 2, 12, 00, tzinfo=timezone('UTC'))


@pytest.mark.django_db
def test_group_user_get_next_order(data_fixture):
    user = data_fixture.create_user()

    assert GroupUser.get_last_order(user) == 1

    group_user_1 = data_fixture.create_user_group(order=0)
    group_user_2_1 = data_fixture.create_user_group(order=10)
    data_fixture.create_user_group(user=group_user_2_1.user, order=11)

    assert GroupUser.get_last_order(group_user_1.user) == 1
    assert GroupUser.get_last_order(group_user_2_1.user) == 12


@pytest.mark.django_db
def test_group_has_user(data_fixture):
    user = data_fixture.create_user()
    user_group = data_fixture.create_user_group()

    assert user_group.group.has_user(user_group.user)
    assert not user_group.group.has_user(user)


@pytest.mark.django_db
def test_group_has_user_with_permissions(data_fixture):
    user = data_fixture.create_user()
    user_group = data_fixture.create_user_group(permissions='ADMIN')

    assert not user_group.group.has_user_with_permissions(user, 'ADMIN')
    assert not user_group.group.has_user_with_permissions(user, ['ADMIN', 'MEMBER'])

    assert not user_group.group.has_user_with_permissions(user_group.user, 'MEMBER')
    assert user_group.group.has_user_with_permissions(user_group.user, 'ADMIN')
    assert user_group.group.has_user_with_permissions(
        user_group.user, ['ADMIN', 'MEMBER']
    )

    user_group.permissions = 'MEMBER'
    user_group.save()

    assert not user_group.group.has_user_with_permissions(user, 'ADMIN')
    assert user_group.group.has_user_with_permissions(user_group.user, 'MEMBER')
    assert user_group.group.has_user_with_permissions(
        user_group.user, ['ADMIN', 'MEMBER']
    )


@pytest.mark.django_db
def test_group_check_user_permissions(data_fixture):
    user = data_fixture.create_user()
    user_group = data_fixture.create_user_group(permissions='ADMIN')

    with pytest.raises(UserInvalidGroupPermissionsError):
        assert not user_group.group.check_user_permissions(user, 'ADMIN')

    with pytest.raises(UserInvalidGroupPermissionsError):
        assert not user_group.group.check_user_permissions(
            user,
            ['ADMIN', 'MEMBER']
        )

    user_group.group.check_user_permissions(user_group.user, 'ADMIN')


@pytest.mark.django_db
def test_application_content_type_init(data_fixture):
    group = data_fixture.create_group()
    database = Database.objects.create(name='Test 1', order=0, group=group)

    assert database.content_type.app_label == 'database'
    assert database.content_type.model == 'database'
