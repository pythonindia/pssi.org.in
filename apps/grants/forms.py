from django.forms import (
    ModelForm,
    MultipleChoiceField,
    SelectMultiple)
from django.contrib.auth.models import User

from django_markdown.fields import MarkdownFormField
from django_markdown.widgets import MarkdownWidget


from .models import GrantRequest, LocalConfRequest, LocalConfComment


def get_all_users():
    return [(user.id, user.username)
            for user in User.objects.order_by('username').all()]


class GrantRequestForm(ModelForm):
    class Meta:
        model = GrantRequest
        exclude = [
            'gtype', 'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]


class LocalConfRequestForm(ModelForm):
    team_members = MultipleChoiceField(
        choices=get_all_users(),
        widget=SelectMultiple(),
        required=False,
        label='Team Members',
        )

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
    class Meta:
        model = LocalConfComment
        fields = ['text']
