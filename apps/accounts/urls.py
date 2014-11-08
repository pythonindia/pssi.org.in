from django.conf.urls import patterns, url
from .views import ProfileView

urlpatterns = patterns(
    '',
    url(r'^$', ProfileView.as_view(), name='profile_home'),
)
