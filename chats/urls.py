from django.urls import path

from chats.views import chat_view

urlpatterns = [
    path('', chat_view),
]