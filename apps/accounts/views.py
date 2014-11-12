from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
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
