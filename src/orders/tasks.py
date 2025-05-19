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

    count_group_name = "orders_count_group"
    message_count_type = 'send_order_count'
    count_payload = len(orders)
    # async_to_sync(channel_layer.group_send)(
    #     count_group_name,
    #     {
    #         'type': message_count_type,
    #         'data': json.dumps(count_payload, default=str)
    #     }
    # ) 

    
    
    
    orders_group_name = "orders_update_group"
    message_orders_type = 'update_orders_table'
    orders_payload = orders
    async_to_sync(channel_layer.group_send)(
        orders_group_name,
        {
            'type': message_orders_type,
            'data': json.dumps(orders_payload, default=str)
        }
    ) 

    print('something good!')
    return order.number

@shared_task
def create_order_every_5_minutes():
    from src.orders.models import get_orders, PosOrder
    from src.orders.utils import create_new_order
    from src.accounts.models import User
    user = User.objects.first()
    order = create_new_order(user)

    orders = get_orders(user=user)

    channel_layer = get_channel_layer()

    count_group_name = "orders_count_group"
    message_count_type = 'send_order_count'
    count_payload = len(orders)
    # async_to_sync(channel_layer.group_send)(
    #     count_group_name,
    #     {
    #         'type': message_count_type,
    #         'data': json.dumps(count_payload, default=str)
    #     }
    # ) 

    
    
    
    orders_group_name = "orders_update_group"
    message_orders_type = 'update_orders_table'
    orders_payload = orders
    async_to_sync(channel_layer.group_send)(
        orders_group_name,
        {
            'type': message_orders_type,
            'data': json.dumps(orders_payload, default=str)
        }
    ) 

    print('something good!')
    return order.number