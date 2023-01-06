import calendar
import django
import datetime

from members.models import Registration
from shares.models import MemberShares
from loans.models import LoanApplication


def members_dict():
    entries = Registration.objects.all()
    dictionary = {i: [] for i in range(1, 13)}
    for entry in entries:
        date = entry.user.date_joined
        month = date.month
        dictionary[month].append(entry)

    return dictionary


def shares_dict():
    entries = MemberShares.objects.all()
    dictionary = {i: [] for i in range(1, 13)}
    for entry in entries:
        date = entry.month_of_contribution
        month = date.month
        dictionary[month].append(entry)

    return dictionary


def loans_dict():
    entries = LoanApplication.objects.all()
    dictionary = {i: [] for i in range(1, 13)}
    for entry in entries:
        date = entry.date_of_application
        month_int = date.month
        month = calendar.month_name[month_int]
        print(month)
        dictionary[month_int].append(entry)

    return dictionary


# from administration.utils import members_dict as dict
# from administration.utils import shares_dict as dict
# from administration.utils import loans_dict as dict


