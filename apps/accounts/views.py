# -*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UserProfile, Membership, MembershipApplication
from .forms import UserProfileForm

from grants.models import GrantRequest
from common.views import LoginRequiredMixin
from common import emailer


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


class MembershipApplyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        application, created = MembershipApplication.objects.get_or_create(
            profile=user.profile)

        if created:
            messages.info(
                self.request, 'We have received the application.')
            # Send email to user and staff
            emailer.send_new_membership_email(user=user)
        else:
            messages.info(
                self.request, 'You have already applied.')

        return redirect(reverse('profile_membership'))


class MembershipView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'profile/membership.html'
    context_object_name = 'membership_history'

    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(
            user_id=self.request.user.pk
        )
        return profile.membership_history.all().select_related()

    def get_context_data(self, **kwargs):
        context = super(MembershipView, self).get_context_data(**kwargs)
        context['user_profile'] = self.request.user.profile
        context['payment_history'] = self.request.user.payment_set.all().select_related()
        return context
