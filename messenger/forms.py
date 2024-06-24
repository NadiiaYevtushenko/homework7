from django import forms
from django.contrib.auth.models import User
from .models import Chat, Message

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'users']
        widgets = {
            'users': forms.CheckboxSelectMultiple,
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']



class MessageEditForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']