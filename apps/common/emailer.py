# -*- coding: utf-8 -*-

"""File contains small function responsible for sending email to various
third parties.
"""

from django.core.mail import send_mail
from django.conf import settings

from .service import get_all_staff_emails


# TODO: Later move this to Django Template
MESSAGE = """
    Hi {first_name}

    {body}

    """

GRANT_DATA = """
    Following are the details submitted for reference:
    -------------------------------------------------
    Grant Type: {instance.gtype.name}
    Event Details: {instance.event_details}
    Event Address: {instance.event_address}
    Event Url: {instance.event_url}
    Event Start Date: {instance.event_date_from}
    Event End Date: {instance.event_date_to}
    Talk Url: {instance.talk_url}
    Requested Amount: {instance.amount}
    Support from Others: {instance.support_from_other}
    Comments: {instance.comments}
    """

FOOTER = """
    Regards
    PSSI - Python Software Society Of India
    """

GRANT_MESSAGE = ''.join([MESSAGE, GRANT_DATA, FOOTER])
APLLICATION_MESSAGE = ''.join([MESSAGE, FOOTER])
PAYMENT_SUCCESS_MESSAGE = ''.join([MESSAGE, FOOTER])


def send_new_grant_email(user, instance):
    """Send email to user and staff when grant is submitted.
    """
    _send_grant_email_to_user(user, instance)
    _send_grant_email_to_staff(user, instance)


def send_update_grant_email(user, instance):
    subject = "PSSI grant request update: {}".format(instance.gtype.name)
    message = """
    Hi {first_name}

    Your grant request is {status}.
    """.format(first_name=user.first_name,
               status=instance.get_status_display().lower())
    return _send_mail(subject=subject, message=message,
                      recipient_list=[user.email])


def send_update_membership_email(user, instance):
    subject = "PSSI membership update"
    if instance.status == 'a':
        payment_message = "Your membership will be complete after making payment."\
                          "Click here {} to make the payment.".format(
                              settings.MEMBERSHIP_PAYMENT_LINK)
    else:
        payment_message = ""

    message = """
    Hi {first_name}

    Your membership is {status}. {payment_message}
    """.format(first_name=user.first_name,
               status=instance.get_status_display().lower(),
               payment_message=payment_message)
    return _send_mail(subject=subject, message=message,
                      recipient_list=[user.email])


def send_new_membership_email(user):
    """Send email to user and staff when grant is submitted.
    """
    _send_new_membership_to_user(user)
    _send_new_membership_to_staff(user)


def send_payment_confirmation_email(user, instance):
    _send_payment_confirmation_email_to_user(user, instance)
    _send_payment_confirmation_email_to_staff(user, instance)


# Private functions
def _send_mail(subject, message, recipient_list):
    """All the email originating from system should go via this interface.
    This is private to the module. All the public functions should call this.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    return send_mail(subject=subject, message=message,
                     from_email=from_email, recipient_list=recipient_list)


def _send_grant_email_to_user(user, instance):
    subject = "PSSI new grant request: {}".format(instance.gtype.name)
    body = """
    Your grant request for amount {amount} is submitted. You'll receive an
    email soon with the status. You can also login into the site and
    check the status of it.""".format(amount=instance.amount)
    message = GRANT_MESSAGE.format(first_name=user.first_name,
                                   amount=instance.amount,
                                   instance=instance,
                                   body=body)
    return _send_mail(subject, message, recipient_list=[user.email])


def _send_grant_email_to_staff(user, instance):
    subject = "PSSI new grant request: {}".format(instance.gtype.name)
    body = """
    {first_name} has submitted grant request for amount: {amount} """.format(
        first_name=user.first_name, amount=instance.amount)
    message = GRANT_MESSAGE.format(first_name=user.first_name,
                                   amount=instance.amount,
                                   instance=instance,
                                   body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())


def _send_new_membership_to_staff(user):
    subject = 'PSSI new membership request'
    body = """
    {first_name} has submitted application to become PSSI member""".format(
        first_name=user.first_name)
    message = APLLICATION_MESSAGE.format(first_name=user.first_name, body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())


def _send_new_membership_to_user(user):
    subject = 'PSSI new membership request'
    body = """
    Your request to become PSSI member is received. We are processing it and
    email will be sent with the updated status.
    """
    message = APLLICATION_MESSAGE.format(first_name=user.first_name, body=body)
    return _send_mail(subject, message, recipient_list=[user.email])


def _send_payment_confirmation_email_to_user(user, instance):
    subject = 'PSSI membership payment successful'
    body = """
    Your payment of Rs.{amount} is successfully received.
    """.format(amount=instance.amount)
    message = PAYMENT_SUCCESS_MESSAGE.format(first_name=user.first_name,
                                             body=body)
    return _send_mail(subject, message, recipient_list=[user.email])


def _send_payment_confirmation_email_to_staff(user, instance):
    subject = 'PSSI membership payment successful'
    body = """
    {first_name}'s membership payment of {amount} successfully received.""".format(
        first_name=user.first_name, amount=instance.amount)
    message = PAYMENT_SUCCESS_MESSAGE.format(first_name=user.first_name,
                                             body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())
