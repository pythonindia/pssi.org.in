from django import forms

from pagedown.widgets import PagedownWidget
from .models import GrantRequest, LocalConfRequest, LocalConfComment

LOCAL_CONF_HELP_TEXT = """
Give us more information about the conference. These details are target audience,
event structure, sponsors, partners, local community, previous events details, WiFi, Transport, accomodation etc ...

Take your time and fill the application. The markdown format is supported
"""


class GrantRequestForm(forms.ModelForm):
    class Meta:
        model = GrantRequest
        exclude = [
            'gtype', 'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]


class LocalConfRequestForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget(show_preview=True),
                            help_text=LOCAL_CONF_HELP_TEXT)
    class Meta:
        model = LocalConfRequest
        exclude = [
            'requester', 'transferred_amount', 'status', 'created_at', 'updated_at'
        ]

    def clean_status(self):
        data = self.cleaned_data['status']
        if data:
            return data
        return 'p'

    def clean_upload(self):
        ALLOWED_FORMATS = (".pdf", ".ods", ".xlsx")
        file = self.cleaned_data.get('upload')
        if not file._get_name().endswith(ALLOWED_FORMATS):
            raise forms.ValidationError(
                "Allowed formats are {}".format(ALLOWED_FORMATS))
        return file


class LocalConfBoardRequestForm(forms.ModelForm):
    class Meta:
        model = LocalConfRequest
        fields = ['status', 'transferred_amount']


class LocalConfCommentForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget(show_preview=True),
                     help_text=LOCAL_CONF_HELP_TEXT)
    class Meta:
        model = LocalConfComment
        fields = ['text']
