from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import UserProfile, Membership
from .forms import UserProfileForm
from common.views import LoginRequiredMixin


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
