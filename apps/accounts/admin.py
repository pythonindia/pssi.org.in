from django.contrib import admin
from .models import UserProfile, Membership


admin.site.register([UserProfile, Membership])
