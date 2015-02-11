from django.forms import ModelForm
from .models import Nomination


class NominationForm(ModelForm):

    class Meta:
        model = Nomination
        exclude = ['ntype', 'user']
