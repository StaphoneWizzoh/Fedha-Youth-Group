from allauth.account.forms import SignupForm
from django import forms
# from django.contrib.auth.models import AbstractUser

from .models import Registration, Guarantor, MemberExit, User


class RegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegistrationForm, self).__init__(*args, **kwargs)
        user, pk = User.objects.filter(id=self.request.user.pk),self.request.user.pk
        print(user)
        self.fields['user'].queryset = User.objects.filter(id=pk)

    class Meta:
        model = Registration
        exclude = ('date_joined',)

    # Registration validations
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        user_age = cleaned_data.get('age')
        user_reg_fee = cleaned_data.get('registration_fee')
        user_id = cleaned_data.get('id_number')
        user_contact = cleaned_data.get('contact_number')

        if user_age is not None and user_reg_fee is not None and user_id is not None and user_contact is not None:
            if user_age < 18 or user_age > 35:
                self.add_error('age',
                               'Only youths can be registered in the society.')

            if user_reg_fee != 1000:
                self.add_error('registration_fee', 'The registration fee allowed is KSH.1000.')

            if len(str(user_id)) != 8:
                self.add_error('id_number', 'Please enter a valid Kenyan ID number')

            if '+' not in str(user_contact):
                self.add_error('contact_number', 'Please enter a valid contact number with format "+254*********".')


class GuarantorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(GuarantorForm, self).__init__(*args, **kwargs)
        self.fields['guarantor_name'].queryset = Registration.objects.filter(
            user=self.request.user
        )
        self.fields['beneficiary_name'].queryset = Registration.objects.exclude(
            user=self.request.user
        )

    class Meta:
        model = Guarantor
        exclude = ('date',)
        confirmation = forms.BooleanField(help_text="Are you sure you want to guarantee the person")


class MemberExitForm(forms.ModelForm):
    class Meta:
        model = MemberExit
        exclude = ('application_date',)
