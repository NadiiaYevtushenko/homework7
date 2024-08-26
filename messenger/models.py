from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} is {"online" if self.is_online else "offline"}'


class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='chats')

    def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        if not user.is_superuser:
            raise PermissionDenied("Only superusers can remove users from chat.")
        self.users.remove(user)


    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def can_edit(self, user):
        return self.author == user or user.is_superuser

    def edit_message(self, new_content, user):
        if self.can_edit(user):
            self.content = new_content
            self.save()
        else:
            raise PermissionDenied("You cannot edit this message.")

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'