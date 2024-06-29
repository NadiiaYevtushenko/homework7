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


class AddUserForm(forms.Form):
    username = forms.CharField(label='Username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)