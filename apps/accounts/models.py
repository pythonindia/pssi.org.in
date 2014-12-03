from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.utils import DatabaseError
from django.db.models import Q
from django.utils.functional import cached_property
from common.models import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile"
    )
    profession = models.CharField(
        help_text="What do you do?",
        max_length=200,
        default="I work/study at ..."
    )
    about = models.TextField(
        help_text="Few lines about yourself",
        default="I like ..."
    )
    github_url = models.URLField(blank=True, null=True)
    bitbucket_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    learned_about_pssi = models.TextField(
        "How did you come to know about PSSI?",
        default="I came to know about PSSI from ..."
    )

    def __str__(self):
        return self.user.get_full_name()

    @cached_property
    def is_pssi_member(self):
        now = timezone.now()
        return self.membership_history.filter(
            from_date__lte=now,
            to_date__gte=now,
        ).count() > 0


class MembershipApplication(BaseModel):
    APPLICATION_STATUS_CHOICES = (
        ('u', 'Under Review'),
        ('a', 'Approved'),
        ('r', 'Rejected'),
    )

    profile = models.OneToOneField(
        'UserProfile'
    )
    status = models.CharField(
        "Membership Application Status", max_length=1,
        choices=APPLICATION_STATUS_CHOICES, default='u'
    )

    def __str__(self):
        return "<{} of {}, status: {}>".format(self.__class__.__name__,
                                               self.profile,
                                               self.get_status_display())


class Membership(BaseModel):
    PAYMENT_METHOD_CHOICES = (
        ('on', 'Online'),
        ('off', 'Offline'),
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
