# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from common import emailer
from board.models import BoardMember

from .models import (GrantRequest, GrantType,
                     LocalConfRequest, LocalConfComment)
from .forms import (GrantRequestForm, LocalConfRequestForm,
                    LocalConfBoardRequestForm, LocalConfCommentForm)


def is_board_member(user):
    return BoardMember.objects.filter(user=user).exists()


def can_participate_in_discussion(local_conf, user):
    return is_board_member(user)


class GrantTypeListView(ListView):
    model = GrantType
    template_name = 'grants/list.html'
    context_object_name = 'grants_list'

    def get_queryset(self):
        return self.model.objects.filter(active=True).order_by('id')


class GrantRequestCreateView(CreateView):
    model = GrantRequest
    form_class = GrantRequestForm
    template_name = 'grants/apply_grants.html'
    success_url = reverse_lazy('grants_req_success')

    def get_context_data(self, *args, **kwargs):
        context = super(
            GrantRequestCreateView, self).get_context_data(*args, **kwargs)
        context['gtype'] = get_object_or_404(
            GrantType, pk=self.kwargs.get('gtype_id'), active=True)
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.status = 'p'
        form.instance.gtype_id = self.kwargs.get('gtype_id')
        # Send email to user and staff
        emailer.send_new_grant_email(user=user,
                                     instance=form.instance)
        return super(GrantRequestCreateView, self).form_valid(form)


class LocalConfCreateView(CreateView):
    model = LocalConfRequest
    form_class = LocalConfRequestForm
    template_name = 'grants/local_conf_apply.html'

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.instance.status = 'p'
        # Send email to user and staff
        local_conf = form.save()

        url = reverse('local_conf_detail', args=[local_conf.pk])
        messages.add_message(self.request, messages.INFO,
                             'New local conf grant request created.')

        emailer.send_new_local_conf_email(
            local_conf=local_conf, user=self.request.user,
            send_to=local_conf.get_all_participants(),
            url=self.request.build_absolute_uri(url))
        return redirect(url)


class LocalConfDetailView(CreateView):
    model = LocalConfRequest
    form_class = LocalConfCommentForm
    template_name = 'grants/local_conf_detail.html'
    success_url = reverse_lazy('local_conf_detail')

    def get_object(self, pk):
        return get_object_or_404(
            LocalConfRequest, pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        local_conf = self.get_object(pk)
        if can_participate_in_discussion(local_conf, request.user):
            comments = LocalConfComment.objects.filter(
                local_conf=local_conf).order_by('id')
            ctx = {'form': self.form_class(),
                   'local_conf': local_conf,
                   'comments': comments}
            return render(request, self.template_name, ctx)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        local_conf = self.get_object(pk)
        if can_participate_in_discussion(local_conf, request.user):
            form = self.form_class(data=request.POST)
            if form.is_valid():
                comment = LocalConfComment(user=request.user,
                                           text=form.cleaned_data['text'],
                                           local_conf=local_conf)
                comment.save()
                url = reverse('local_conf_detail', args=[local_conf.pk])
                emailer.send_local_conf_comment_email(
                    local_conf=local_conf, user=request.user,
                    send_to=local_conf.get_all_participants(),
                    url=request.build_absolute_uri(url))
                messages.add_message(request, messages.INFO,
                                     'Your comment successfully recorded.')
                return redirect(url)
            else:
                comments = LocalConfComment.objects.filter(
                local_conf=local_conf).order_by('id')
                ctx = {'form': self.form_class(),
                       'local_conf': local_conf,
                       'comments': comments}
                return render(request, self.template_name, ctx)
        return HttpResponseForbidden()


class LocalConfDownloadAttachmentView(DetailView):
    model = LocalConfRequest
    pk_url_kwargs = 'pk'
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        if not obj.upload:
            return HttpResponse('No attachment to download')
        if can_participate_in_discussion(obj, self.request.user):
            filename = obj.upload.name.split('/')[-1]
            response = HttpResponse(
                obj.upload.file,
                content_type=obj.get_content_type())
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                filename.replace(' ', '_'))
            return response
        return HttpResponseForbidden()
