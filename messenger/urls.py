from django.urls import path
from .views import ChatListView, chat_detail, chat_create, edit_message, add_user_to_chat
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chat/new/', chat_create, name='chat_create'),
    path('message/<int:message_id>/edit/', edit_message, name='edit_message'),
    path('chat/<int:chat_id>/add_user/', add_user_to_chat, name='add_user_to_chat'),
]
