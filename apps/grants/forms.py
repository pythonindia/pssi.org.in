from django.forms import (
    ModelForm,
    CharField,
    MultipleChoiceField,
    Textarea,
    SelectMultiple)

from pagedown.widgets import PagedownWidget
from .models import GrantRequest, LocalConfRequest, LocalConfComment

LOCAL_CONF_HELP_TEXT = """
Give us more information about the conference. These details are target audience,
event structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...

Take your time and fill the application. The markdown format is supported
"""


class GrantRequestForm(ModelForm):
    class Meta:
        model = GrantRequest
        exclude = [
            'gtype', 'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]


class LocalConfRequestForm(ModelForm):
    description = CharField(widget=PagedownWidget(show_preview=True),
                            help_text=LOCAL_CONF_HELP_TEXT)
    note = CharField(widget=PagedownWidget(show_preview=True),
                     help_text="Any specific note to the board")

    class Meta:
        model = LocalConfRequest
        exclude = [
            'requester', 'transferred_amount', 'status', 'created_at', 'updated_at'
        ]

    def clean_team_members(self):
        data = self.cleaned_data['team_members']
        if data:
            return User.objects.filter(pk__in=data)
        return None

    def clean_status(self):
        data = self.cleaned_data['status']
        if data:
            return data
        return 'p'


class LocalConfBoardRequestForm(ModelForm):
    class Meta:
        model = LocalConfRequest
        fields = ['status', 'transferred_amount']


class LocalConfCommentForm(ModelForm):
    text = CharField(widget=PagedownWidget(show_preview=True),
                     help_text=LOCAL_CONF_HELP_TEXT)
    class Meta:
        model = LocalConfComment
        fields = ['text']
