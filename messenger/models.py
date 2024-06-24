from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_edit_message", "Can edit message"),
            ("can_delete_message", "Can delete message"),
        ]

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'