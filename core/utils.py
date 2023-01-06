from datetime import datetime
from django.db import transaction
from django.db.models import Sum, Count, F

from members.models import Registration
from shares.models import MemberShares
from shares.utils import total_shares
from loans.models import LoanApplication, LoanRepayment
from loans.utils import get_loan_id, expected_monthly_payment, last_balance


def end_year():
    month_int = datetime.now().month
    day_int = datetime.now().day
    if (month_int == 12) and (day_int >= 20):
        return True
    else:
        return False


def all_shares():
    total = MemberShares.objects.aggregate(Sum('amount'))['amount__sum']
    return total


def total_loans():
    total = LoanApplication.objects.aggregate(Sum('loan_amount'))['loan_amount__sum']
    return total


def total_deposits():
    deposits = all_shares() - total_loans()
    return deposits


def total_loans_interest():
    repaid_sum = LoanRepayment.objects.aggregate(Sum('amount'))['amount__sum']
    print(repaid_sum)
    interest = repaid_sum - total_loans()
    return interest


def deposits_revenue(year):
    p = all_shares() - total_loans()
    total = p * (pow((0.006 + 1), year))
    return total - p


def loans_revenue():
    return 100


def total_revenue(year):
    total = deposits_revenue(year) + loans_revenue()
    return total


def office_expenses(year):
    total = total_revenue(year) * 0.1
    return total


def total_dividends(year):
    total = total_revenue(year) * 0.9
    return total


def individual_dividends(member_id):
    if end_year():
        ratio = total_shares(member_id) / all_shares()
        dividend = ratio * total_dividends(1)
        return dividend


def dividends_disbursement():
    members = Registration.objects.select_for_update().all()
    with transaction.atomic():
        for member in members:
            if total_shares(member.id) is not None:
                shareholder = Registration.objects.get(user__id=member.id)
                MemberShares.objects.create(member_name=shareholder, amount=individual_dividends(member.id))


def repayment_schedules():
    loans = LoanApplication.objects.all()
    schedule = {}
    for loan in loans:
        schedule[str(loan.applicant_name)] = expected_monthly_payment(loan.id)

    return schedule


def repayment_balances():
    balances = {}
    loaners = LoanApplication.objects.filter(paid=False)
    for loaner in loaners:
        balances[str(loaner.applicant_name)] = last_balance(loaner.applicant_name.id, get_loan_id(loaner.applicant_name.id))

    return balances


def test():
    loaners = LoanApplication.objects.filter(paid=False)
    for loaner in loaners:
        print(loaner.applicant_name)

# from core.utils import repayment_balances as rb
