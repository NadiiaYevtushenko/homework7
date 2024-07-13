from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import MessageForm
from .models import Message
from django.http import JsonResponse

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = User.objects.get(is_superuser=True)
            message.save()

            if message.recipient.is_superuser:
                messages.success(request, "Ви успішно надіслали повідомлення суперюзеру")

            return JsonResponse({
                'status': 'success',
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

    else:
        form = MessageForm()

    return redirect('chat:dialog')

@login_required
def dialog(request):
    admin_user = User.objects.get(is_superuser=True)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=admin_user)) |
        (Q(sender=admin_user) & Q(recipient=request.user))
    ).order_by('timestamp')
    form = MessageForm()
    return render(request, 'chat/dialog.html', {'messages': messages, 'form': form, 'admin_user_id': admin_user.id, 'user': request.user})