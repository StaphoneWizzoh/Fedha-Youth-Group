from django.db import models

from shares.utils import total_shares_count, total_shares
from members.models import Registration


class LoanTypes(models.Model):
    type = models.CharField(max_length=15)
    interest = models.FloatField(max_length=5)
    repayment_period = models.IntegerField(help_text="In Years.")

    class Meta:
        verbose_name_plural = 'Loan Types'

    @property
    def max_amount(self):
        if self.type.lower() == "normal":
            return total_shares(member_id) * 3
        elif self.type.lower() == 'emergency':
            return total_shares(member_id)
        elif self.type.lower() == "short":
            return total_shares(member_id) * 2
        elif self.type.lower() == 'development':
            return total_shares(member_id) * 5

    def __str__(self):
        return self.type


class LoanApplication(models.Model):
    applicant_name = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date_of_application = models.DateTimeField(auto_now_add=True)
    loan_type = models.ForeignKey(LoanTypes, on_delete=models.CASCADE)
    loan_amount = models.IntegerField(help_text="Amount you want to borrow.")
    expected_interest = models.FloatField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.applicant_name


class LoanRepayment(models.Model):
    payee_id = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date_of_repayment = models.DateTimeField(auto_now_add=True)
    loan_id = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount you want to repay.")
    loan_balance = models.FloatField(help_text="Your loan balance.")

    def __str__(self):
        return self.payee_id.user.username
