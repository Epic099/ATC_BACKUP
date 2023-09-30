from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/<str:room>/', consumers.AtcConsumer.as_asgi())
]