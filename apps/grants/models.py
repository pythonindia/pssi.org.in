from django.db import models
from django.conf import settings
from common.models import BaseModel
from board.models import BoardMember

from django_markdown.models import MarkdownField


GRANT_STATUS_CHOICES = (
    ('p', 'PENDING'),
    ('a', 'ACCEPTED'),
    ('r', 'REJECTED'),
    ('c', 'CANCELLED'),
)

LOCAL_CONF_STATUS_CHOICES = (
    ('p', 'PENDING'),
    ('a', 'ACCEPTED'),
    ('r', 'REJECTED'),
    ('c', 'CANCELLED'),
    ('t', 'TRANSFERRED'),
)

LOCAL_CONF_HELP_TEXT = """
Give us more information about the conference. These details are target audience,
event structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...

Take your time and fill the application. The markdown format is supported
"""


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


class LocalConfRequest(BaseModel):
    name = models.CharField(max_length=100, unique=False,
                            help_text="Name of your event")
    start_date = models.DateField(
        help_text="Enter in following format: YYYY-MM-DD")
    end_date = models.DateField(
        help_text="Enter in following format: YYYY-MM-DD")
    website = models.URLField(help_text="Your event website.",
        blank=True, null=True)
    location_url = models.URLField(help_text="Your event location URL.",
        blank=True, null=True)
    location_address = models.TextField(help_text="Venue address with the venue name")
    required_amount = models.FloatField("Requested amount in INR")
    transferred_amount = models.FloatField("Transferred amount in INR", default=0)
    budget = models.FloatField("Conference budget")
    expected_audience = models.IntegerField("Total expected participants")
    description = MarkdownField("Say us about the conference",
                                help_text=LOCAL_CONF_HELP_TEXT)
    is_brand_new = models.BooleanField(help_text="Is the event held for the first time?",
                                       default=True)
    note = MarkdownField(help_text="Any specific note to the board",
                         null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=LOCAL_CONF_STATUS_CHOICES, db_index=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_all_participants(self):
        """Get all members who have access to the object.
        """
        users = [member.user for member in BoardMember.objects.all()]
        team_members = [member.team_member
                        for member in LocalConfTeamMember.objects.filter(local_conf=self)]
        users.extend(team_members)
        return users

    def __str__(self):
        return "{name}: {start_date} - {end_date} [{status}] by {user}".format(
            name=self.name, start_date=self.start_date, end_date=self.end_date,
            status=self.get_status_display(), user=self.requester)


class LocalConfTeamMember(BaseModel):
    local_conf = models.ForeignKey(LocalConfRequest)
    team_member = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "Local Conf: {local_conf} team member {user}".format(
            local_conf=self.local_conf, user=self.team_member)


class LocalConfComment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = MarkdownField(help_text="Leave your comment and opinion")
    is_system_message = models.BooleanField(default=False)
    local_conf = models.ForeignKey(LocalConfRequest, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment `{text}` by user: {user}".format(text=self.text, user=self.user)
