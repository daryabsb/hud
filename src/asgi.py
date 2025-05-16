import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import src.routing as routing  # We’ll create this

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

application = get_asgi_application()

# Define your WebSocket routing
websocket_routing = URLRouter(
    routing.websocket_urlpatterns
)

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
