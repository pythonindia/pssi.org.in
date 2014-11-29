from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import GrantType, GrantRequest


class GrantTypeAdmin(MarkdownModelAdmin):
    list_display = ('__str__', 'active')
    list_editable = ('active', )


class GrantRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')

admin.site.register(GrantType, GrantTypeAdmin)
admin.site.register(GrantRequest, GrantRequestAdmin)
