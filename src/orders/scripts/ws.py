import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run():
    channel_layer = get_channel_layer()
    group_name = "order_error_notification"
    message_type = 'send_error'
    message = 'This is a websocket message'
    payload = message
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': message_type,
            'data': json.dumps(payload, default=str)
        }
    ) 