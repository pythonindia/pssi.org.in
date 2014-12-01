# -*- coding: utf-8 -*-

from django.contrib.auth.models import User


def get_all_staff_emails():
    """Return all staff emails
    """
    return User.objects.filter(is_staff=True).values_list('email', flat=True)
