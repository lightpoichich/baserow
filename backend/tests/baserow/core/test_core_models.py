import pytest

from baserow.core.models import GroupUser


@pytest.mark.django_db
def test_group_user_get_next_order(data_fixture):
    group_user_1 = data_fixture.create_user_group(order=0)
    group_user_2_1 = data_fixture.create_user_group(order=10)
    group_user_2_2 = data_fixture.create_user_group(user=group_user_2_1.user, order=11)

    assert GroupUser.get_last_order(group_user_1.user) == 1
    assert GroupUser.get_last_order(group_user_2_1.user) == 12
