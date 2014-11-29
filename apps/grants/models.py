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
    name = models.CharField(max_length=100, unique=True)
    terms = models.TextField("Terms & Conditions", blank=True, null=True)
    active = models.BooleanField(
        "Whether this grant type should be available to public",
        default=True
    )

    def __str__(self):
        return self.name


class GrantRequest(BaseModel):
    """
    Grant requests
    """
    gtype = models.ForeignKey('GrantType')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event_details = models.TextField()
    event_address = models.TextField()
    event_url = models.URLField(blank=True, null=True)
    event_date_to = models.DateField(
        help_text="Enter in following format: YYYY-MM-DD")
    event_date_from = models.DateField(
        help_text="Enter in following format: YYYY-MM-DD")
    talk_url = models.URLField(
        help_text="Your talk/session should be accepted already for the grant \
        request to be processed.",
        blank=True, null=True
    )
    amount = models.FloatField("Requested amount")
    granted_amount = models.FloatField(default=0)
    support_from_other = models.TextField(
        "Support from others (if any)",
        help_text="If you've received any financial help from any other \
            organization, please mention.",
        blank=True, null=True
    )
    comments = models.TextField(
        help_text="If you have anything else to mention, please do it here.",
        blank=True, null=True
    )
    status = models.CharField(
        max_length=1, choices=GRANT_STATUS_CHOICES, db_index=True)

    def __str__(self):
        return "{user}: {gtype} [{status}]".format(
            user=self.user.username,
            gtype=self.gtype.name,
            status=self.get_status_display()
        )
