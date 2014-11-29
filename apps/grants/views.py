from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from .models import GrantRequest, GrantType
from .forms import GrantRequestForm


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
        form.instance.user = self.request.user
        form.instance.status = 'p'
        form.instance.gtype_id = self.kwargs.get('gtype_id')
        return super(GrantRequestCreateView, self).form_valid(form)
