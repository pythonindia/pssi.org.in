# -*- coding: utf-8 -*-

from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy

from .models import Nomination, NominationType
from .forms import NominationForm
from common import emailer


class NominationTypeListView(ListView):
    model = NominationType
    template_name = 'nominations/list.html'
    context_object_name = 'nomination_type_list'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(active=True).order_by('id')


class NominationCreateView(CreateView):
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
        emailer.send_new_nomiation_email(
            user=user,
            instance=form.instance
        )
        return super(NominationCreateView, self).form_valid(form)
