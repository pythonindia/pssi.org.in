# -*- coding: utf-8 -*-

from django.conf import settings


def get_all_staff_emails():
    """Return all staff emails
    """
    return settings.STAFF_EMAILS
