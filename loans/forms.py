import sys
from copy import deepcopy
from django import forms

from .models import LoanTypes, LoanApplication, LoanRepayment
from .utils import get_loan_id, expected_monthly_payment

from members.models import Registration
from shares.utils import total_shares as ts


class ApplicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['applicant_name'].queryset = Registration.objects.filter(
            user=self.request.user
        )

    class Meta:
        model = LoanApplication
        exclude = ('date_of_application', 'paid', 'expected_interest')

    # Validations
    def clean(self):
        cleaned_data = super(ApplicationForm, self).clean()
        loan_type = cleaned_data.get('loan_type')
        loan_amount = cleaned_data.get('loan_amount')
        pk = self.request.user.pk
        field = 'loan_amount'
        display_error = "Please apply an amount that is within your shares bracket."

        if loan_type.type == "Normal":
            max_amount = ts(pk) * 3
            if loan_amount > max_amount:
                self.add_error(field, display_error)
        elif loan_type.type == "Emergency":
            max_amount = ts(pk)
            if loan_amount > max_amount:
                self.add_error(field, display_error)
        elif loan_type.type == "Short":
            max_amount = ts(pk) * 2
            if loan_amount > max_amount:
                self.add_error(field, display_error)
        elif loan_type.type == "Development":
            max_amount = ts(pk) * 4
            if loan_amount > max_amount:
                self.add_error(field, display_error)


class RepaymentForm(forms.Form):
    amount = forms.FloatField(help_text="Enter the amount", required=True)

    # def __init__(self, *args, **kwargs, ):
    #     super(RepaymentForm, self).__init__(*args, **kwargs)
    #
    #     temp = deepcopy(args)
    #     self.member_id = temp[1]
    #     pk = self.member_id
    #     # print(args)
    #     print(pk)
    #
    # # def clean(self):
    # #     cleaned_data = super(RepaymentForm, self).clean()
    # #     member_id = self.member_id
    # #     expected_amount = expected_monthly_payment(get_loan_id(member_id))
    # #     paid_amount = cleaned_data.get('amount')
    # #     field = 'amount'
    # #     display_error = "Please pay the least required amount for your borrowed loan."
    # #
    # #     if paid_amount is not None and expected_amount is not None:
    # #         if paid_amount < expected_amount:
    # #             self.add_error(field, display_error)
