from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'about', 'github_url', 'bitbucket_url'
        )
