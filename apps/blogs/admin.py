from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    # slug should be prepopulated from the title
    prepopulated_field = {'slug': ('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
