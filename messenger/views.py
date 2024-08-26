from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ChatForm,  MessageForm, MessageEditForm, LoginForm, AddUserForm
from .models import Chat, Message
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from django.views import View
from .forms import SignUpForm
from .models import UserStatus
from django.http import JsonResponse
from django.contrib.auth.models import User

class ChatListView(ListView):
    model = Chat
    template_name = 'messenger/chat_list.html'
    context_object_name = 'chats'
    paginate_by = 3


@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.users.all():
        return HttpResponseForbidden("You do not have access to this chat.")

    messages = chat.message_set.all()
    for message in messages:
        message.can_user_edit = message.can_edit(request.user)  # Додаємо атрибут до кожного повідомлення

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat = chat
            new_message.author = request.user
            new_message.save()
            return redirect('chat_detail', chat_id=chat_id)
    else:
        form = MessageForm()

    return render(request, 'messenger/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form,
    })


@permission_required('messenger.add_chat')
@user_passes_test(lambda u: u.is_superuser)
def chat_create(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            return redirect('chat_list')
    else:
        form = ChatForm()
    return render(request, 'messenger/chat_form.html', {'form': form})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if request.user != message.author:
        return render(request, 'messenger/edit_message_error.html')

    if request.method == 'POST':
        form = MessageEditForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=message.chat.pk)
    else:
        form = MessageEditForm(instance=message)

    return render(request, 'messenger/edit_message.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat_list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def add_user_to_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            chat.users.add(user)
            return redirect('chat_detail', chat_id=chat_id)
    else:
        form = AddUserForm()

    return render(request, 'messenger/add_user_to_chat.html', {'chat': chat, 'form': form})


class SignupView(View):
    @staticmethod
    def get(request):
        form = SignUpForm()
        return render(request, 'registration/registration.html', {'form': form})

    @staticmethod
    def post(request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_list')
        return render(request, 'registration/registration.html', {'form': form})


@login_required
def check_user_status(request, username):
    try:
        user = get_object_or_404(User, username=username)
        user_status = UserStatus.objects.get(user=user)
        return JsonResponse({'is_online': user_status.is_online})
    except UserStatus.DoesNotExist:
        return JsonResponse({'is_online': False})