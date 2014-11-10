from django.conf.urls import patterns, url
from .views import ProfileView, GrantRequestListView

urlpatterns = patterns(
    '',
    url(r'^$', ProfileView.as_view(), name='profile_home'),
    url(r'^grants/$', GrantRequestListView.as_view(), name='profile_grantreq_list'),
)
