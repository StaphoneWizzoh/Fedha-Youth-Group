from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import user_passes_test, login_required

from .forms import RegistrationForm, MemberExitForm, GuarantorForm
from .models import Registration
from .utils import get_username

from shares.utils import total_shares_count as tsc
from loans.utils import has_existing_loan as hel


def index(request):
    return HttpResponse("<h1>Members App :)</h1>")


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'members/registration.html'
    success_url = 'home'


class MemberUpdateView(UpdateView):
    model = Registration
    template_name = 'members/update.html'
    fields = [
        'first_name', 'last_name',
        'contact_number', 'photo',
    ]

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('members:details', kwargs={'pk': user_id})


class MembersListView(ListView):
    model = Registration
    template_name = 'members/members_list.html'
    context_object_name = 'members'


# @login_required(login_url='account_login')
class MemberDetailView(DetailView):
    model = Registration
    template_name = 'members/member_detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        if tsc(pk) >= 6:
            eligible = True
        else:
            eligible = False
        existing_loan = hel(pk)
        context['eligibility'] = eligible
        context['existing_loan'] = existing_loan
        context['name'] = get_username(pk)
        return context


class GuarantorView(CreateView):
    form_class = GuarantorForm
    template_name = 'members/guarantor.html'
    context_object_name = 'guarantor'

    def get_form_kwargs(self):
        kwargs = super(GuarantorView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('members:details', kwargs={'pk': user_id})


def member_exit(request, pk):
    context = {}
    return render(request, 'members/exit.html', context)
