from django.forms import ModelForm, ModelChoiceField, CharField
from .models import GrantRequest, GrantType


class GrantRequestForm(ModelForm):
    gtype = ModelChoiceField(
        required=True,
        label="Grant Type",
        empty_label=None,
        queryset=GrantType.objects.all().order_by('id')
    )

    class Meta:
        model = GrantRequest
        exclude = [
            'user', 'granted_amount', 'status', 'created_at', 'updated_at'
        ]
