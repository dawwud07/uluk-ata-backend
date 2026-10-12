from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import SimpleTestCase

from apps.Profile.consumers import NotificationsConsumer
from apps.Profile.middleware import TokenAuthMiddleware


class NotificationsConsumerTests(SimpleTestCase):
	async def test_authenticated_user_receives_private_notification(self):
		user = SimpleNamespace(is_authenticated=True, pk=42)
		consumer_application = NotificationsConsumer.as_asgi()

		async def authenticated_application(scope, receive, send):
			await consumer_application({**scope, 'user': user}, receive, send)

		communicator = WebsocketCommunicator(authenticated_application, '/ws/notifications/')
		connected, _ = await communicator.connect()
		self.assertTrue(connected)

		notification = {'id': 7, 'title': 'Order accepted'}
		await get_channel_layer().group_send(
			'user_42_notifications',
			{'type': 'notification.created', 'data': notification},
		)
		self.assertEqual(await communicator.receive_json_from(), notification)
		await communicator.disconnect()

	async def test_anonymous_user_is_rejected(self):
		consumer_application = NotificationsConsumer.as_asgi()

		async def anonymous_application(scope, receive, send):
			user = SimpleNamespace(is_authenticated=False)
			await consumer_application({**scope, 'user': user}, receive, send)

		communicator = WebsocketCommunicator(anonymous_application, '/ws/notifications/')
		connected, close_code = await communicator.connect()
		self.assertFalse(connected)
		self.assertEqual(close_code, 4401)

	@patch('apps.Profile.middleware.get_user_from_token', new_callable=AsyncMock)
	async def test_api_token_authenticates_websocket(self, get_user_from_token):
		user = SimpleNamespace(is_authenticated=True, pk=42)
		get_user_from_token.return_value = user
		application = TokenAuthMiddleware(NotificationsConsumer.as_asgi())
		communicator = WebsocketCommunicator(
			application,
			'/ws/notifications/?token=existing-api-token',
		)

		connected, _ = await communicator.connect()
		self.assertTrue(connected)
		get_user_from_token.assert_awaited_once_with('existing-api-token')
		await communicator.disconnect()
