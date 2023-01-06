import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, models
from django.db.models import Q, Sum

from members.models import Registration
from loans.models import LoanApplication, LoanRepayment, LoanTypes


def first_time_repay(member_id, loan_id):
    counter = LoanRepayment.objects.filter(Q(payee_id=member_id) & Q(loan_id=loan_id)).count()
    return counter


def last_balance(member_id, loan_id):
    value = LoanRepayment.objects.filter(Q(payee_id=member_id) & Q(loan_id=loan_id)).last()
    return value.loan_balance


def interest(loan_id):
    loan = LoanApplication.objects.get(id=loan_id)
    loan_interest = loan.loan_type.interest
    interest_earned = loan.loan_amount * loan_interest
    return int(interest_earned)


def get_loan_type(loan_id):
    loan = LoanApplication.objects.get(id=loan_id)
    loan_type = loan.loan_type.type
    return loan_type


def get_loan_date(loan_id):
    loan = LoanApplication.objects.get(id=loan_id)
    date = str(loan.date_of_application)
    cutter = date.find('.')
    loan_date = date[:cutter]
    return loan_date


def get_loan_id(member_id):
    member = Registration.objects.get(user__id=member_id)
    try:
        loan = LoanApplication.objects.filter(Q(applicant_name=member) & Q(paid=False)).get(applicant_name=member)
        return loan.id
    except ObjectDoesNotExist:
        return None


def repay(member_id, loan_id, amount):
    member = Registration.objects.get(user__id=member_id)
    loan = LoanApplication.objects.get(id=loan_id)
    loan_entries = LoanApplication.objects.select_for_update().filter(id=loan_id)
    with transaction.atomic():
        for entry in loan_entries:
            curr_loan_amount = LoanApplication.objects.get(id=loan_id)
            loan_interest = loan.loan_type.interest
            total_repaid = LoanRepayment.objects.filter(payee_id=member).aggregate(Sum('amount'))['amount__sum']

            if first_time_repay(member_id, loan_id) == 0:
                balance = (curr_loan_amount.loan_amount * (loan_interest + 1)) - amount
            else:
                balance = last_balance(member_id, loan_id) - amount
            LoanRepayment.objects.create(amount=amount, loan_id=loan,
                                         payee_id=member, loan_balance=balance)
            if balance == 0:
                LoanApplication.objects.filter(id=loan_id).update(paid=True)
                LoanApplication.objects.filter(id=loan_id).update(paid=True)


def has_existing_loan(member_id):
    try:
        LoanApplication.objects.get(Q(applicant_name=member_id) & Q(paid=False))
        return True
    except ObjectDoesNotExist:
        return False


def expected_monthly_payment(loan_id):
    loan = LoanApplication.objects.get(id=loan_id)
    total_loan_amount = (interest(loan_id)) + loan.loan_amount
    months = loan.loan_type.repayment_period * 12
    payable_amount = total_loan_amount / months
    return payable_amount
