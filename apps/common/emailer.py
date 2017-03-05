# -*- coding: utf-8 -*-

"""File contains small function responsible for sending email to various
third parties.

# Note:

Code can have been organized into single function say `send_email(user, instance, type)`,
where `type` is the type of the email, then
function will have `if, elif` block. Depending on type, call separate function.
I wasn't quite happy with that approach. In future maintainer can feel free to rewrite.
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

NOMINATION_DATA = """
    Following are the details submitted for reference:
    -------------------------------------------------
    Nomination Type: {instance.ntype.name}
    Nominee Name: {instance.fullname}
    Nominee Email: {instance.email}
    Nominee Gender: {instance.gender}
    Nominee Profession: {instance.profession}
    Nominee Contributions: {instance.contribution_info}
    References: {instance.references}
    """
FOOTER = """
    Regards
    PSSI - Python Software Society Of India
    """

NEW_LOCAL_CONF = """
    Hi {first_name}

    {user.first_name} has submitted new local conf grant request.

    The complete details is available at: {url}

    Note: Please don't reply to the email.
"""

LOCAL_CONF_COMMENT = """
    Hi {first_name}

    {user.first_name} has submitted a new comment.

    The complete details is available at: {url}

    Note: Please don't reply to the email.
"""


GRANT_MESSAGE = ''.join([MESSAGE, GRANT_DATA, FOOTER])
NOMINATION_MESSAGE = ''.join([MESSAGE, NOMINATION_DATA, FOOTER])

APPLICATION_MESSAGE = ''.join([MESSAGE, FOOTER])
PAYMENT_SUCCESS_MESSAGE = ''.join([MESSAGE, FOOTER])

NEW_LOCAL_CONF_MESSAGE = ''.join([NEW_LOCAL_CONF, FOOTER])
LOCAL_CONF_COMMENT_MESSAGE = ''.join([LOCAL_CONF_COMMENT, FOOTER])


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


def send_voting_email(user, nomination_type, slug, vote_url):
    subject = "PSSI Voting Request for {nomination_type} - {slug}".format(nomination_type=nomination_type, 
                                                                          slug=slug)
    message = """ 
                    Hi %s,

                    As you are aware that we have closed the Nomination for %s - %s.

                    We are in the process of voting. Being a PSSI member, your vote makes a lot of difference.
                    Below is the link for voting.
                    <a href="%s">Vote</a>
                    Request you to vote for a nominee and help us select one.

                    Cheers!
                    PSSI Board.
                    """ % (user.first_name, nomination_type, slug, vote_url)

    return _send_mail(subject, message, recipient_list=[user.email])


def send_local_conf_comment_email(local_conf, user, send_to, url):
    subject = "New comment on local conf: {}".format(local_conf.name)
    for receiver in send_to:
        message = LOCAL_CONF_COMMENT_MESSAGE.format(
            user=user, url=url, first_name=receiver.first_name)
        _send_mail(subject=subject, message=message, recipient_list=[receiver.email])


def send_new_local_conf_email(local_conf, user, send_to, url):
    subject = "New local conf grant request: {}".format(local_conf.name)
    for receiver in send_to:
        message = NEW_LOCAL_CONF_MESSAGE.format(
            user=user, url=url, first_name=receiver.first_name)
        _send_mail(subject=subject, message=message, recipient_list=[receiver.email])


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
    # We don't want list of staffs to be addressed with someone's first name
    message = GRANT_MESSAGE.format(first_name="",
                                   amount=instance.amount,
                                   instance=instance,
                                   body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())


def _send_new_membership_to_staff(user):
    subject = 'PSSI new membership request'
    body = """
    {first_name} has submitted application to become PSSI member""".format(
        first_name=user.first_name)
    # We don't want list of staffs to be addressed with someone's first name
    message = APPLICATION_MESSAGE.format(first_name="", body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())


def _send_new_membership_to_user(user):
    subject = 'PSSI new membership request'
    body = """
    Your request to become PSSI member is received. We are processing it and
    email will be sent with the updated status.
    """
    message = APPLICATION_MESSAGE.format(first_name=user.first_name, body=body)
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
    # We don't want list of staffs to be addressed with someone's first name
    message = PAYMENT_SUCCESS_MESSAGE.format(first_name="",
                                             body=body)
    return _send_mail(subject, message, recipient_list=get_all_staff_emails())


def _send_new_nomiation_email_to_user(user, instance):
    subject = "[PSSI] New nomination request: {}".format(instance.ntype.name)
    body = """
    We have received you nomintation for {fullname}
    Thanks you for your nomination""".format(fullname=instance.fullname)
    message = NOMINATION_MESSAGE.format(
        first_name=user.first_name,
        instance=instance,
        body=body
    )
    return _send_mail(subject, message, recipient_list=[user.email])


def _send_new_nomiation_email_to_staff(user, instance):
    subject = "[PSSI] New nomination request: {}".format(instance.ntype.name)
    body = """
    {first_name} has submitted nomintation for : {fullname} """.format(
        first_name=user.first_name, fullname=instance.fullname)
    # We don't want list of staffs to be addressed with someone's first name
    message = NOMINATION_MESSAGE.format(
        first_name='',
        instance=instance,
        body=body
    )
    return _send_mail(subject, message, recipient_list=['contact@pssi.org.in'])


def send_new_nomiation_email(user, instance):
    """Send email to user and staff when grant is submitted.
    """
    _send_new_nomiation_email_to_user(user, instance)
    _send_new_nomiation_email_to_staff(user, instance)
