# -*- coding: utf-8 -*-

"""File contains small function responsible for sending email to various
third parties.
"""

from django.core.mail import send_mail
from django.conf import settings

from .service import get_all_staff_emails


# TODO: Later move this to Django Template
GRANT_MESSAGE = """
    Hi {first_name}

    {body}

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


def send_new_grant_email(user, instance):
    _send_grant_email_to_user(user, instance)
    _send_grant_email_to_staff(user, instance)


# Private functions
def _send_mail(subject, message, recipient_list):
    """All the email originating from system should go via this interface.
    This is private to the module. All the public functions should call this.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    return send_mail(subject=subject, message=message,
                     from_email=from_email, recipient_list=recipient_list)


def _send_grant_email_to_user(user, instance):
    subject = "PSSI New Grant Request: {}".format(instance.gtype.name)
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
    subject = "PSSI New Grant Request: {}".format(instance.gtype.name)
    body = """
    {first_name} has submitted grant request for amount: {amount} """.format(
        first_name=user.first_name, amount=instance.amount)
    message = GRANT_MESSAGE.format(first_name=user.first_name,
                                   amount=instance.amount,
                                   instance=instance,
                                   body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())
