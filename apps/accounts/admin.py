# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import UserProfile, Membership, MembershipApplication

from common import emailer


class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('get_username', 'created_at', 'from_date', 'to_date')

    def get_username(self, obj):
        return obj.profile.user.username
    get_username.short_description = 'User'
    get_username.admin_order_field = 'profile__user__username'


class MembershipApplicationAdmin(admin.ModelAdmin):
    model = MembershipApplication
    list_display = ('get_username', 'created_at', 'get_status_display')
    readonly_fields = ('profile', 'show_url')

    list_filter = ['status']
    actions = ['send_membership_status_email']

    def get_username(self, obj):
        return obj.profile.user.username
    get_username.short_description = 'User'
    get_username.admin_order_field = 'profile__user__username'

    def show_url(self, instance):
        return '<a target="_blank" href="%s">%s</a>' % ('/admin/accounts/userprofile/%d/' % instance.profile.pk, 'Go to profile')
    show_url.short_description = 'User Profile Details'
    show_url.allow_tags = True

    def send_membership_status_email(self, request, action_objects):
        for action_object in action_objects:
            emailer.send_update_membership_email(action_object.profile.user,
                                                 instance=action_object)
        self.message_user(request, "Membership update email is sent.")


admin.site.register(Membership, MembershipAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register([UserProfile])
