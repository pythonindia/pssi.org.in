from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from grants.views import GrantRequestCreateView, GrantTypeListView
from nominations.views import NominationCreateView, NominationTypeListView
from nominations.views import NomineeListView
from board.views import BoardListView

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', TemplateView.as_view(
        template_name='index.html',
    ), name='home'),
    url(r'^about/$', BoardListView.as_view(), name='about-static'),
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
    url(r'^financial/$', TemplateView.as_view(
        template_name='financial.html',
    ), name='financial'),
    url(r'^pymonth/$', TemplateView.as_view(
        template_name='python_month.html',
    ), name='pymonth'),
    url(r'^miniconf/$', TemplateView.as_view(
        template_name='mini_conf.html',
    ), name='miniconf'),

    url(r'^grants/list/$', GrantTypeListView.as_view(),
        name='grants_list'),
    url(r'^grants/apply/(?P<gtype_id>[\d]+)/$',
        GrantRequestCreateView.as_view(), name='grants_apply'),
    url(r'^grants/apply-success/$', TemplateView.as_view(
        template_name='grants/apply_grants_success.html',
    ), name='grants_req_success'),
    url(r'^nomination/list/$',
        login_required(NominationTypeListView.as_view()),
        name='nomination_list'),
    url(r'^nomination/nominee/(?P<slug>[\w+]+)/list/$',
        login_required(NomineeListView.as_view()),
        name='view_nominations'),
    url(r'^nomination/success/$', login_required(TemplateView.as_view(
        template_name='nominations/nomination_success.html')),
        name='nominee_req_success'),

    url(r'^nomination/(?P<slug>[\w+]+)/$',
        login_required(NominationCreateView.as_view()),
        name='create_nominee'),

    url(r'^blog/', include('blogs.urls')),
    url(r'^profile/', include('accounts.urls')),
    url(r'^payment/', include('payments.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
)
