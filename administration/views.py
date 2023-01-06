from datetime import datetime
from django.shortcuts import render

from blogs.models import Post
from members.models import Registration
from loans.models import LoanApplication, LoanRepayment
from shares.models import MemberShares
from core.utils import (all_shares, total_deposits, total_dividends,
                        total_loans, repayment_schedules, repayment_balances)


def index(request):
    members = Registration.objects.order_by('-last_name')[0:5]
    members_num = Registration.objects.count()
    shares = MemberShares.objects.order_by('-amount')[0:10]
    deposits = total_deposits
    loans = total_loans
    recent_posts = Post.objects.order_by('-timestamp')[0:10]

    context = {
        'members': members,
        'members_number': members_num,
        'shares': shares,
        'deposits': deposits,
        'loans': loans,
        'recents': recent_posts,
    }

    return render(request, 'administration/index.html', context)


def error_404(request, exception):
    return render(request, 'administration/pages-error-404.html')


def error_500(request, exception):
    return render(request, 'administration/pages-error-500.html')


def registrations(request):
    members = Registration.objects.all()
    context = {
        'members': members
    }

    return render(request, 'administration/members.html', context)


def contributions(request):
    shares = MemberShares.objects.all()
    total = all_shares
    context = {
        'shares': shares,
        'total': total,
    }

    return render(request, 'administration/contributions.html', context)


def deposits(request):
    shares = MemberShares.objects.all()
    total = total_deposits
    context = {
        'shares': shares,
        'total': total,
    }
    return render(request, 'administration/deposits.html', context)


def loans(request):
    all_loans = LoanApplication.objects.all()
    context = {
        'loans': all_loans,
    }
    return render(request, 'administration/loans.html', context)


def schedules(request):
    schedule = repayment_schedules()
    context = {
        'schedule': schedule,
    }
    return render(request, 'administration/schedules.html', context)


def balances(request):
    balance = repayment_balances()
    context = {
        'balances': balance,
    }
    return render(request, 'administration/balances.html', context)


def dividends(request):
    context = {
        'year': datetime.now().year,
        'dividends': total_dividends(1)
    }
    return render(request, 'administration/dividends.html', context)
