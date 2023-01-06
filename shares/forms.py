from django import forms
from django.contrib.auth.models import User
from django.db import models

from members.models import Registration
from .models import MemberShares


class SharesForm(forms.ModelForm):
    are_you_sure = forms.BooleanField(required=True,)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SharesForm, self).__init__(*args, **kwargs)
        self.fields['member_name'].queryset = Registration.objects.filter(
            user=self.request.user
        )

    class Meta:
        model = MemberShares
        exclude = ('date_of_contribution',)

    def clean(self):
        cleaned_data = super(SharesForm, self).clean()
        user_amount = cleaned_data.get('amount')
        user = cleaned_data.get('member_name')

        if user_amount is not None:
            if user_amount < 500:
                self.add_error('amount',
                               'The minimum contribution amount is KSH.500.')

