from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['users']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'author', 'timestamp', 'content']
    list_filter = ['chat', 'author']
    search_fields = ['content']
