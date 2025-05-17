from src.orders.models import PosOrder
from celery import shared_task
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def create_order_every_5_minutes():
    from src.orders.models import get_orders, PosOrder
    from src.orders.utils import create_new_order
    from src.accounts.models import User
    user = User.objects.first()
    order = create_new_order(user)

    orders = get_orders(user=user)

    channel_layer = get_channel_layer()
    group_name = "order_error_notification"
    message_type = 'send_error'
    payload = len(orders)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': message_type,
            'data': json.dumps(payload, default=str)
        }
    ) 
    print('something good!')
    return payload