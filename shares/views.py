from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import (
    CreateView, ListView, DetailView)

from .forms import SharesForm
from .models import MemberShares
from .utils import total_shares as ts, total_shares_count as tsc

from members.models import Registration,User
from members.utils import get_username
from loans.utils import has_existing_loan as hel


def index(request):
    return HttpResponse("<h1>Shares App :)</h1>")


class ContributionView(CreateView):
    form_class = SharesForm
    template_name = 'shares/contribution.html'

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('shares:details', kwargs={'pk': user_id})

    def get_form_kwargs(self):
        kwargs = super(ContributionView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SharesDetailview(DetailView):
    template_name = 'shares/detail.html'
    model = MemberShares
    context_object_name = 'shares'

    # def get_object(self, queryset=None):
    #     pk = self.request.user.pk
    #     user = User.objects.get(pk=pk)
    #     member = Registration.objects.get(user=user)
    #     share = MemberShares.objects.filter(member_name=member)
    #     return share

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        if tsc(pk) >= 6:
            eligible = True
        else:
            eligible = False
        total = ts(pk)
        existing_loan = hel(pk)
        context['total'] = total
        context['eligibility'] = eligible
        context['existing_loan'] = existing_loan
        context['name'] = get_username(pk)
        return context
