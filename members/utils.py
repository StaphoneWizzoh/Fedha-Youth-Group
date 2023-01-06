from django.db.models import Sum, Count, F
from .models import Registration, Guarantor


def get_user_id():
    user = Registration.objects.get(email=f"{User.email}")
    return user.id


def total_guaranteed_amount(member_id):
    member = Registration.objects.get(user__id=member_id)
    total = Guarantor.objects.filter(beneficiary_name=member). \
        aggregate(Sum('amount_guaranteed'))['amount_guaranteed__sum']
    return total


def get_username(member_id):
    member = Registration.objects.get(user__id=member_id)
    return member.first_name + " " + member.last_name
