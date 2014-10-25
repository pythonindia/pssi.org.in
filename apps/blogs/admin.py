from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import Post, Tag


class PostAdmin(MarkdownModelAdmin):
    # slug should be prepopulated from the title
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
