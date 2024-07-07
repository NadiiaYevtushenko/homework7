from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'content')
    list_filter = ('timestamp',)


admin.site.register(Message, MessageAdmin)
