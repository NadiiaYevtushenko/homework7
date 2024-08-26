from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from messenger.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageDetailSerializer


class UserChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        username = self.kwargs['username']
        chat = get_object_or_404(Chat, id=chat_id, users=self.request.user)
        return Message.objects.filter(chat=chat, author__username=username)


class UserChatsView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(users=self.request.user)


class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id, users=self.request.user)
        return Message.objects.filter(chat=chat)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фільтр - тільки ті повідомлення, до яких користувач має доступ
        return Message.objects.filter(chat__users=self.request.user)


class CreateMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id, users=self.request.user)
        serializer.save(author=self.request.user, chat=chat)

