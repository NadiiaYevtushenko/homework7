from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from messenger.models import Message


class PaginationMixin:
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['object_list'], self.paginate_by)
        try:
            context['object_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['object_list'] = paginator.page(1)
        except EmptyPage:
            context['object_list'] = paginator.page(paginator.num_pages)
        context['is_paginated'] = paginator.num_pages > 1
        context['paginator'] = paginator
        return context



class MessageAuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=kwargs['message_id'])
        if request.user != message.author:
            return HttpResponseForbidden("You do not have permission to edit this message.")
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

