import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string, get_template
from django.template import Template

class OrdersCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders_count_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders_count_group", self.channel_name)

    async def send_order_count(self, event):
        data = event['data']

        received_data = json.loads(data)
        # received_data = 5
        html = get_template('cotton/ws/count.html').render(
            context={'count': received_data}
        )
        # html = await sync_to_async(render_to_string)('cotton/ws/count.html', {'count': received_data})
        await self.send(text_data=html)

class OrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders_update_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders_update_group", self.channel_name)

    async def update_orders_table(self, event):
        data = event['data']

        received_data = json.loads(data)
        # received_data = 5
        html = get_template('cotton/ws/pos_tabs_orders_table.html').render(
            context={'orders': received_data, 'count': len(received_data)}
        )
        # html = await sync_to_async(render_to_string)('cotton/ws/count.html', {'count': received_data})
        await self.send(text_data=html)

