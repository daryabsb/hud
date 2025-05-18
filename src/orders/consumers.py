import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string, get_template
from django.template import Template

class OrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("order_error_notification", self.channel_name)
        await self.channel_layer.group_add("order_success_notification", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_error_notification", self.channel_name)
        await self.channel_layer.group_discard("order_success_notification", self.channel_name)
    
    async def send_error(self, event):
        data = event['data']

        received_data = json.loads(data)
        # received_data = 5
        html = get_template('cotton/ws/count.html').render(
            context={'count': received_data}
        )
        # html = await sync_to_async(render_to_string)('cotton/ws/count.html', {'count': received_data})
        await self.send(text_data=html)

