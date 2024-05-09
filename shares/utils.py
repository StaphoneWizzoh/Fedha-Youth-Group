from datetime import datetime
from django.db.models import Sum, Count, F
from django.db.models.functions import \
    (ExtractMonth, TruncMonth, Greatest, Least)

from members.models import Registration
from .models import MemberShares


# returns total shares of an individual
def total_shares(member_id):
    member = Registration.objects.get(user__id=member_id)
    total = MemberShares.objects.filter(member_name=member). \
        aggregate(Sum('amount'))['amount__sum']
    return total


# returns sum of shares of an individual per month
def shares_total_per_month(member_id):
    member = Registration.objects.get(user__id=member_id)
    total = MemberShares.objects.filter(member_name=member). \
        annotate(month=TruncMonth('month_of_contribution')).values('month'). \
        annotate(total=Count('member_name'))
    return total


# returns aggregate count of shares per month
def shares_count_per_month(member_id):
    member = Registration.objects.get(user__id=member_id)
    count = MemberShares.objects.filter(member_name=member). \
        aggregate(Count('month_of_contribution'))['month_of_contribution__count']
    return count


# returns count of share contribution 
def total_shares_count(member_id):
    member = Registration.objects.get(user__id=member_id)
    count = MemberShares.objects.filter(member_name=member, month_of_contribution__month__gte=6).count()
    return count


