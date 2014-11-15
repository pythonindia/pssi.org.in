from django.conf.urls import patterns, url
from .views import PostList, PostDetails

urlpatterns = patterns(
    '',
    url(r'^$', PostList.as_view(), name='blog_archive'),
    url(r'^(?P<slug>[a-z0-9\-]+)/$', PostDetails.as_view(), name='blog_post'),
)
