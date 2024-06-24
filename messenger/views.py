from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ChatForm, MessageForm
from .models import Chat, Message


@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    if request.user not in chat.users.all():
        return redirect('chat_list')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', pk=chat.pk)
    else:
        form = MessageForm()

    messages = chat.message_set.all()
    return render(request, 'messenger/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})


@permission_required('messenger.add_chat')
def chat_create(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            return redirect('chat_list')
    else:
        form = ChatForm()
    return render(request, 'messenger/chat_form.html', {'form': form})
