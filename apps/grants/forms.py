from django.forms import ModelForm, ModelChoiceField, CharField
from .models import GrantRequest, GrantType


class GrantRequestForm(ModelForm):
    class Meta:
        model = GrantRequest
        exclude = [
            'gtype', 'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]
