from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'blogs/archive.html'
    context_object_name = 'post_list'


class PostDetails(DetailView):
    model = Post
    template_name = 'blogs/post.html'
    context_object_name = 'post'
