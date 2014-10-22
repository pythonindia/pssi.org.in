from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from .models import GrantRequest
from .forms import GrantRequestForm


class GreatRequestCreateView(CreateView):
    model = GrantRequest
    form_class = GrantRequestForm
    template_name = 'grants/apply_grants.html'
    success_url = reverse_lazy('grants_req_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'p'
        return super(GreatRequestCreateView, self).form_valid(form)
