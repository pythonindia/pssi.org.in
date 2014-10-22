from django.contrib import admin
from .models import GrantType, GrantRequest


admin.site.register(GrantType)
admin.site.register(GrantRequest)
