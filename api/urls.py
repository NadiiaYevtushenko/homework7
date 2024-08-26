from django.urls import path
from .views import UserChatsView, ChatMessagesView, MessageDetailView, CreateMessageView, UserChatMessagesView

urlpatterns = [
    path('chats/', UserChatsView.as_view(), name='user-chats'),   #всі чати
    path('chats/<int:chat_id>/messages/', ChatMessagesView.as_view(), name='chat-messages'),  # по id чату
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),    # Ендпоінт для перегляду, редагування, видалення повідомлення
    path('chats/<int:chat_id>/messages/create/', CreateMessageView.as_view(), name='create-message'),# для створення повідомлення в чаті
    path('chats/<int:chat_id>/messages/<str:username>/', UserChatMessagesView.as_view(), name='user-chat-messages'),# для перегляду конкретного користувача і його всіх повідомлень по чату
]