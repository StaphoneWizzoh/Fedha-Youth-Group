from django.urls import path

from .views import index, ApplicationView, repayment

app_name = 'loans'

urlpatterns = [
    path('', index, name='home'),
    path('application/', ApplicationView.as_view(), name='application'),
    # path('repayment/', RepaymentView.as_view(), name='repayment'),
    path('repayment/', repayment, name='repayment'),

]
