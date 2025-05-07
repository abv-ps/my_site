from django.urls import path

from chats.ws.consumers import ChatConsumer

socket_urlpatterns = [path('ws/chat/<str:group_name>/', ChatConsumer.as_asgi())]