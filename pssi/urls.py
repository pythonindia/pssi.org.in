from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(
        template_name='index.html',
    ), name='home'),
    url(r'^pyconindia/$', TemplateView.as_view(
        template_name='pyconindia.html',
    ), name='pyconindia-static'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)
