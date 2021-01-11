from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CoreConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

        user = self.scope['user']
        web_socket_id = self.scope['web_socket_id']

        await self.send_json({
            'type': 'authentication',
            'success': user is not None,
            'web_socket_id': web_socket_id
        })

        if not user:
            await self.close()
            return

        await self.channel_layer.group_add('users', self.channel_name)

    async def receive(self, message):
        pass

    async def disconnect(self, message):
        await self.channel_layer.group_discard('users', self.channel_name)

    async def broadcast_to_users(self, event):
        web_socket_id = self.scope['web_socket_id']
        payload = event['payload']
        user_ids = event['user_ids']
        ignore_web_socket_id = event['ignore_web_socket_id']

        if (
            (not ignore_web_socket_id or ignore_web_socket_id != web_socket_id) and
            self.scope['user'].id in user_ids
        ):
            await self.send_json(payload)
