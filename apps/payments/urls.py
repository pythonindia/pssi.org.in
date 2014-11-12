from django.conf.urls import patterns, url
from .views import (MembershipPaymentConfirmView)

urlpatterns = patterns(
    '',
    url(r'^confirm/membership/$', MembershipPaymentConfirmView.as_view(), name='payment_membership_confirm'),
)
