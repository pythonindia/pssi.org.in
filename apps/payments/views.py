import json
from datetime import timedelta

from django.views.generic.base import RedirectView, View
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages

from common.views import CSRFExemptMixin, LoginRequiredMixin
from common import emailer
from .models import (Payment, PaymentGateway, PaymentType)
from accounts.models import Membership, UserProfile, MembershipApplication

from instamojo import Instamojo


class MembershipPaymentConfirmView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # get payment details from payment id
        payment_id = self.request.GET.get('payment_id', '')
        if not payment_id:
            return reverse('profile_membership') + "?status=fail"

        im = PaymentGateway.objects.get(name='Instamojo')
        api = Instamojo(
            api_key=im.api_key,
            auth_token=im.auth_token
        )
        resp = api.payment_detail(payment_id=payment_id)
        print(resp)
        payment_resp = resp.get('payment', {})
        print(payment_resp)

        if not resp.get('success', False) or not payment_resp:
            return reverse('profile_membership') + "?status=fail"

        # create payment instance
        payment, created = Payment.objects.get_or_create(
            gateway=im,
            payment_id=payment_id,
            ptype=PaymentType.objects.get(name__iexact='membership'),
        )
        payment.user_id = self.request.user.pk
        payment.amount = float(payment_resp.get('amount'))
        payment.status = 'r'  # received
        payment.status_pg = payment_resp.get('status')
        payment.raw_details = json.dumps(payment_resp)
        payment.save()

        # check pament status
        success = (self.request.GET.get('status') == 'success' and
                   payment_resp.get('status') == 'Credit')
        # if success create membership instance
        if success:
            now = timezone.now()
            profile = self.request.user.profile
            membership = Membership(
                profile=profile,
                from_date=now,
                to_date=now + timedelta(days=365 * 2),
                payment=payment
            )
            membership.save()

            membershipapplication = profile.membershipapplication
            membershipapplication.status = 'a'
            membershipapplication.save()

            messages.info(
                self.request, 'Your payment has been successfully received.')

            # send email to staff and user
            emailer.send_payment_confirmation_email(
                user=self.request.user, instance=payment)
            return reverse('profile_membership') + "?status=success"
        # else show error
        else:
            messages.info(
                self.request, 'Something went wrong when processing your payment. Please contact us at contact@pssi.org.in')
            return reverse('profile_membership') + "?status=fail"
