from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import Nomination, NominationType


class AdminNominationType(MarkdownModelAdmin):
    list_display = ('__str__', 'active')
    list_editable = ('active',)


class NominationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    list_filter = ['ntype__slug']
    actions = ['export_nomination_to_csv']

    def export_nomination_to_csv(self, request, action_objects):
        # TODO  Need to work on this action Kept it as place holder
        pass
admin.site.register(
    NominationType,  AdminNominationType)
admin.site.register(Nomination, NominationAdmin)
