# -*- coding: utf-8 -*-
from datetime import datetime
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Nomination, NominationType
from .forms import NominationForm
from common import emailer
from board.models import BoardMember


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
                                            request,  *args, **kwargs)


def is_board_member(user):
    if BoardMember.objects.filter(
                        user=user).exists():
        return True
    return False


class NominationTypeListView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/list.html'
    context_object_name = 'nomination_type_list'

    def get_context_data(self, *args, **kwargs):
        context = super(
            NominationTypeListView, self).get_context_data(*args, **kwargs)
        context['nomination_type_list'] = NominationType.objects.filter(active=True).order_by('id')
        context['board_member'] = is_board_member(self.request.user)
        return context


class NomineeListView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/nominee_list.html'
    context_object_name = 'nomination_type_list'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Not board Member")
        return super(NomineeListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            NomineeListView, self).get_context_data(*args, **kwargs)
        nomination_type = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        context['nomination_list'] = Nomination.objects.filter(ntype=nomination_type)
        return context


class NominationCreateView(CreateView, LoginRequiredMixin):
    model = Nomination
    form_class = NominationForm
    template_name = 'nominations/nominations.html'
    success_url = reverse_lazy('nominee_req_success')

    def get_context_data(self, *args, **kwargs):
        context = super(
            NominationCreateView, self).get_context_data(*args, **kwargs)
        context['ntype'] = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        return context

    def get_form(self, *args, **kwargs):
        form = super(NominationCreateView, self).get_form(self.form_class)
        ntype = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        if ntype.name == 'Kenneth Gonsalves':
            form.fields.popitem('reason_to_join_board')
        return form

    def __init__(self, *args, **kwargs):
        super(NominationCreateView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.ntype = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        emailer.send_new_nomiation_email(user=user,
                                     instance=form.instance)
        return super(NominationCreateView, self).form_valid(form)
