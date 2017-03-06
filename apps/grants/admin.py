from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import (GrantType, GrantRequest, LocalConfRequest,
                     LocalConfComment)

from common import emailer


class GrantTypeAdmin(MarkdownModelAdmin):
    list_display = ('__str__', 'active')
    list_editable = ('active', )


class LocalConfRequestAdmin(MarkdownModelAdmin):
    pass


class GrantRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    actions = ['send_request_status_email']
    list_filter = ['status']

    def send_request_status_email(self, request, action_objects):
        for action_object in action_objects:
            emailer.send_update_grant_email(action_object.user, action_object)
        self.message_user(request, "Grant update email is sent.")


class LocalConfCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(GrantType, GrantTypeAdmin)
admin.site.register(GrantRequest, GrantRequestAdmin)
admin.site.register(LocalConfRequest, LocalConfRequestAdmin)
admin.site.register(LocalConfComment, LocalConfCommentAdmin)
