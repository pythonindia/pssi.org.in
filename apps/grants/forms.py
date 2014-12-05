from django.forms import ModelForm
from .models import GrantRequest


class GrantRequestForm(ModelForm):
    class Meta:
        model = GrantRequest
        exclude = [
            'gtype', 'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]
