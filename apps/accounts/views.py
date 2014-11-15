from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from .models import UserProfile, Membership
from .forms import UserProfileForm
from common.views import LoginRequiredMixin
from grants.models import GrantRequest


class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profile/home.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile_home')

    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(
            user_id=self.request.user.pk
        )
        return profile

    def form_valid(self, form):
        User = get_user_model()
        user = User.objects.get(pk=form.instance.user_id)
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        user.save()
        return super(ProfileView, self).form_valid(form)

    def get_initial(self):
        initial = self.initial.copy()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_profile'] = self.object
        return context


class GrantRequestListView(LoginRequiredMixin, ListView):
    model = GrantRequest
    template_name = 'profile/grantreq_list.html'
    context_object_name = 'grantrequest_list'

    def get_queryset(self):
        return self.request.user.grantrequest_set.all()


class MembershipView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'profile/membership.html'
    context_object_name = 'membership_history'

    def get_queryset(self):
        return self.request.user.profile.membership_history.all()

    def get_context_data(self, **kwargs):
        context = super(MembershipView, self).get_context_data(**kwargs)
        context['user_profile'] = self.request.user.profile
        return context
