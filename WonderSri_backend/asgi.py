"""
ASGI config for WonderSri_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django  # ✅ Ensure Django is initialized before importing anything else

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WonderSri_backend.settings')

django.setup()  # ✅ Load Django before importing anything that depends on it

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tracking.routing  # ✅ Import after Django is fully set up

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tracking.routing.websocket_urlpatterns
        )
    ),
})

app = application  # ✅ This is fine if needed for external use
