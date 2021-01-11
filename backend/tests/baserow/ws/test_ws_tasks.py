import pytest

from asgiref.sync import sync_to_async

from channels.testing import WebsocketCommunicator

from baserow.config.asgi import application
from baserow.ws.tasks import broadcast_to_users, broadcast_to_group


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_broadcast_to_users(data_fixture):
    user_1, token_1 = data_fixture.create_user_and_token()
    user_2, token_2 = data_fixture.create_user_and_token()

    communicator_1 = WebsocketCommunicator(
        application,
        f'ws/core/?jwt_token={token_1}',
        headers=[(b"origin", b"http://localhost")]
    )
    await communicator_1.connect()
    response_1 = await communicator_1.receive_json_from()
    web_socket_id_1 = response_1['web_socket_id']

    communicator_2 = WebsocketCommunicator(
        application,
        f'ws/core/?jwt_token={token_2}',
        headers=[(b"origin", b"http://localhost")]
    )
    await communicator_2.connect()
    response_2 = await communicator_2.receive_json_from()
    response_2['web_socket_id']

    await sync_to_async(broadcast_to_users)([user_1.id], {'message': 'test'})
    response_1 = await communicator_1.receive_json_from(0.01)
    await communicator_2.receive_nothing(0.01)
    assert response_1['message'] == 'test'

    await sync_to_async(broadcast_to_users)(
        [user_1.id, user_2.id],
        {'message': 'test'},
        ignore_web_socket_id=web_socket_id_1
    )
    await communicator_1.receive_nothing(0.01)
    response_2 = await communicator_2.receive_json_from(0.01)
    assert response_2['message'] == 'test'

    assert communicator_1.output_queue.qsize() == 0
    assert communicator_2.output_queue.qsize() == 0

    await communicator_1.disconnect()
    await communicator_2.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_broadcast_to_group(data_fixture):
    user_1, token_1 = data_fixture.create_user_and_token()
    user_2, token_2 = data_fixture.create_user_and_token()
    user_3, token_3 = data_fixture.create_user_and_token()
    user_4, token_4 = data_fixture.create_user_and_token()
    group_1 = data_fixture.create_group(users=[user_1, user_2, user_4])
    group_2 = data_fixture.create_group(users=[user_2, user_3])

    communicator_1 = WebsocketCommunicator(
        application,
        f'ws/core/?jwt_token={token_1}',
        headers=[(b"origin", b"http://localhost")]
    )
    await communicator_1.connect()
    response_1 = await communicator_1.receive_json_from()
    web_socket_id_1 = response_1['web_socket_id']

    communicator_2 = WebsocketCommunicator(
        application,
        f'ws/core/?jwt_token={token_2}',
        headers=[(b"origin", b"http://localhost")]
    )
    await communicator_2.connect()
    response_2 = await communicator_2.receive_json_from()
    web_socket_id_2 = response_2['web_socket_id']

    communicator_3 = WebsocketCommunicator(
        application,
        f'ws/core/?jwt_token={token_3}',
        headers=[(b"origin", b"http://localhost")]
    )
    await communicator_3.connect()
    await communicator_3.receive_json_from()

    await sync_to_async(broadcast_to_group)(group_1.id, {'message': 'test'})

    response_1 = await communicator_1.receive_json_from(0.01)
    response_2 = await communicator_2.receive_json_from(0.01)
    communicator_3.receive_nothing(0.01)

    assert response_1['message'] == 'test'
    assert response_2['message'] == 'test'

    await sync_to_async(broadcast_to_group)(
        group_1.id,
        {'message': 'test2'},
        ignore_web_socket_id=web_socket_id_1
    )

    await communicator_1.receive_nothing(0.01)
    response_2 = await communicator_2.receive_json_from(0.01)
    await communicator_3.receive_nothing(0.01)

    assert response_2['message'] == 'test2'

    await sync_to_async(broadcast_to_group)(
        group_2.id,
        {'message': 'test3'},
        ignore_web_socket_id=web_socket_id_2
    )

    await communicator_1.receive_nothing(0.01)
    await communicator_2.receive_nothing(0.01)
    await communicator_3.receive_json_from(0.01)

    assert communicator_1.output_queue.qsize() == 0
    assert communicator_2.output_queue.qsize() == 0
    assert communicator_3.output_queue.qsize() == 0

    await communicator_1.disconnect()
    await communicator_2.disconnect()
    await communicator_3.disconnect()
