from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.utils import DatabaseError
from django.db.models import Q
from common.models import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile"
    )
    about = models.TextField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    bitbucket_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def is_pssi_member(self):
        now = timezone.now()
        return self.membership_history.filter(
            from_date__lte=now,
            to_date__gte=now,
        ).count() > 0


class Membership(BaseModel):
    PAYMENT_METHOD_CHOICES = (
        ('on', 'Online'),
        ('off', 'Offline'),
    )
    MEMBERSHIP_STATUS_CHOICES = (
        ('u', 'Under Review'),
        ('a', 'Approved')
    )

    profile = models.ForeignKey(
        'UserProfile', related_name="membership_history"
    )
    from_date = models.DateField()
    to_date = models.DateField()
    payment = models.ForeignKey('payments.Payment', blank=True, null=True)
    payment_method = models.CharField(
        max_length=3, choices=PAYMENT_METHOD_CHOICES, default='on'
    )
    status = models.CharField(
        "Status", max_length=1, choices=MEMBERSHIP_STATUS_CHOICES, default='u'
    )

    def __str__(self):
        return "{user}, {frm} to {to}".format(
            user=self.profile.user.username,
            frm=self.from_date,
            to=self.to_date
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, **kwargs):
    if kwargs['created'] is True:
        try:
            UserProfile.objects.create(user_id=kwargs['instance'].id)
        except DatabaseError:
            pass


@receiver(post_save, sender=Membership)
def create_membership(sender, **kwargs):
    if kwargs['created'] is True:
        # FIXME: Send mail to staffs
        pass
