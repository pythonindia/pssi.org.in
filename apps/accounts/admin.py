from django.contrib import admin
from .models import UserProfile, Membership


class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('get_username', 'created_at', 'from_date', 'to_date')

    def get_username(self, obj):
        return obj.profile.user.username
    get_username.short_description = 'User'
    get_username.admin_order_field = 'profile__user__username'


admin.site.register(Membership, MembershipAdmin)
admin.site.register([UserProfile])
