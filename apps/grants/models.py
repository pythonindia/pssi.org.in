from django.db import models
from django.conf import settings
from common.models import BaseModel

GRANT_STATUS_CHOICES = (
    ('p', 'PENDING'),
    ('a', 'ACCEPTED'),
    ('r', 'REJECTED'),
    ('c', 'CANCELLED'),
)


class GrantType(BaseModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class GrantRequest(BaseModel):
    """
    Travel Aid requests
    """
    gtype = models.ForeignKey('GrantType')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event_details = models.TextField()
    event_date_to = models.DateTimeField()
    event_date_from = models.DateTimeField()
    talk_url = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    accepted_amount = models.FloatField(default=0)
    support_from_other = models.TextField(blank=True, null=True)
    previous_talk_info = models.TextField(blank=True, null=True)
    granted_support_before = models.BooleanField(default=False)
    granted_support_info = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=GRANT_STATUS_CHOICES, db_index=True)

    def __unicode__(self):
        return "{user}: {status}".format(user=self.user.get_full_name(), status=self.status)
