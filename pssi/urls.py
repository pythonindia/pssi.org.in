from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

from grants.views import GrantRequestCreateView, GrantTypeListView

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', TemplateView.as_view(
        template_name='index.html',
    ), name='home'),
    url(r'^about/$', TemplateView.as_view(
        template_name='about.html',
    ), name='about-static'),
    url(r'^membership/$', TemplateView.as_view(
        template_name='membership.html',
    ), name='membership-static'),
    url(r'^usergroups/$', TemplateView.as_view(
        template_name='user_groups.html',
    ), name='usergroups-static'),
    url(r'^pyconindia/$', TemplateView.as_view(
        template_name='pyconindia.html',
    ), name='pyconindia-static'),
    url(r'^awards/$', TemplateView.as_view(
        template_name='awards.html',
    ), name='awards-static'),
    url(r'^by-laws/$', TemplateView.as_view(
        template_name='by_laws.html',
    ), name='by-laws'),

    url(r'^grants/list/$', GrantTypeListView.as_view(),
        name='grants_list'),
    url(r'^grants/apply/(?P<gtype_id>[\d]+)/$', GrantRequestCreateView.as_view(),
        name='grants_apply'),
    url(r'^grants/apply-success/$', TemplateView.as_view(
        template_name='grants/apply_grants_success.html',
    ), name='grants_req_success'),

    url(r'^blog/', include('blogs.urls')),
    url(r'^profile/', include('accounts.urls')),
    url(r'^payment/', include('payments.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
)
