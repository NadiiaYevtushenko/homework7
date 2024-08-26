from rest_framework import serializers
from messenger.models import Chat, Message
from django.contrib.auth.models import User


class ChatSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'users']


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'content', 'timestamp']


class MessageDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'content', 'timestamp']
