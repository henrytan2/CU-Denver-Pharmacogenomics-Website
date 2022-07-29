"""
ASGI config for DjangoDashProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
from channels.security.websocket import AllowedHostsOriginValidator
from django_plotly_dash.consumers import send_to_pipe_channel
from django_plotly_dash.consumers import async_send_to_pipe_channel
"""
ASGI config for proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoDashProject.settings')
#
# application = get_asgi_application()

ws_pattern = []

application = ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(URLRouter(
        ws_pattern
    ))
})

# application = ProtocolTypeRouter({
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#             ])
#         )
#     ),
# })

