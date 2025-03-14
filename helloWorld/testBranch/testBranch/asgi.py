"""
ASGI config for testBranch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django # ADDED
from django.core.asgi import get_asgi_application
from channels.routing import get_default_application # ADDED
from channels.security.websocket import AllowedHostsOriginValidator # ADDED
import users.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testBranch.settings')
# ADDED
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from users.routing import websocket_urlpatterns
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(), #change to wsgi? add https?
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

# ADDED

django.setup() # ADDED
application = get_default_application() # ADDED
# application = get_asgi_application() #OLD
