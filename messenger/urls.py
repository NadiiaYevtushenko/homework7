from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chat/new/', views.chat_create, name='chat_create'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
]