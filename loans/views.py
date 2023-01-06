from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from .forms import ApplicationForm, RepaymentForm
from .models import LoanApplication
from .utils import repay, get_loan_id, last_balance, interest, get_loan_date, get_loan_type, expected_monthly_payment

from shares.utils import total_shares as ts


def index(request):
    return HttpResponse("<h1>Loans App :)<h1>")


class ApplicationView(CreateView):
    form_class = ApplicationForm
    template_name = 'loans/application.html'
    success_url = reverse_lazy('members:list')
    extra_context = {"max_loan": "max_loan"}

    def get_form_kwargs(self):
        kwargs = super(ApplicationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        normal = ts(pk) * 3
        emergency = ts(pk)
        short = ts(pk) * 2
        development = ts(pk) * 5
        context['normal'] = normal
        context['emergency'] = emergency
        context['short'] = short
        context['development'] = development
        return context


def repayment(request):
    member_id = request.user.pk
    loan_id = get_loan_id(member_id)

    if request.method == "POST":
        form = RepaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            repay(member_id, loan_id, amount)
            return redirect('shares:detail', member_id)

    else:
        form = RepaymentForm(request.GET, member_id)

    loan_interest = interest(loan_id)
    last_loan_balance = last_balance(member_id, loan_id)
    application_date = get_loan_date(loan_id)
    applied_loan_type = get_loan_type(loan_id)

    context = {
        "form": form,
        "interest": loan_interest,
        "balance": last_loan_balance,
        "date": application_date,
        "type": applied_loan_type,
        "expected_amount": expected_monthly_payment(loan_id)

    }
    return render(request, 'loans/repayment.html', context)


class LoanDetail(DetailView):
    model = LoanApplication
