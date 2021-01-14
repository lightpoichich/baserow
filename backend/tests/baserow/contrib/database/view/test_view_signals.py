import pytest

from unittest.mock import patch

from baserow.contrib.database.views.handler import ViewHandler


@pytest.mark.django_db(transaction=True)
@patch('baserow.ws.registries.broadcast_to_channel_group')
def test_view_created(mock_broadcast_to_channel_group, data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    view = ViewHandler().create_view(user=user, table=table, type_name='grid',
                                     name='Grid')

    mock_broadcast_to_channel_group.delay.assert_called_once()
    args = mock_broadcast_to_channel_group.delay.call_args
    assert args[0][0] == f'table-{table.id}'
    assert args[0][1]['type'] == 'view_created'
    assert args[0][1]['view']['id'] == view.id


@pytest.mark.django_db(transaction=True)
@patch('baserow.ws.registries.broadcast_to_channel_group')
def test_view_updated(mock_broadcast_to_channel_group, data_fixture):
    user = data_fixture.create_user()
    view = data_fixture.create_grid_view(user=user)
    ViewHandler().update_view(user=user, view=view, name='View')

    mock_broadcast_to_channel_group.delay.assert_called_once()
    args = mock_broadcast_to_channel_group.delay.call_args
    assert args[0][0] == f'table-{view.table.id}'
    assert args[0][1]['type'] == 'view_updated'
    assert args[0][1]['view_id'] == view.id
    assert args[0][1]['view']['id'] == view.id


@pytest.mark.django_db(transaction=True)
@patch('baserow.ws.registries.broadcast_to_channel_group')
def test_view_deleted(mock_broadcast_to_channel_group, data_fixture):
    user = data_fixture.create_user()
    view = data_fixture.create_grid_view(user=user)
    view_id = view.id
    ViewHandler().delete_view(user=user, view=view)

    mock_broadcast_to_channel_group.delay.assert_called_once()
    args = mock_broadcast_to_channel_group.delay.call_args
    assert args[0][0] == f'table-{view.table.id}'
    assert args[0][1]['type'] == 'view_deleted'
    assert args[0][1]['view_id'] == view_id
