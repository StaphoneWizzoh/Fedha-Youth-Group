from django.contrib import admin

from .models import LoanTypes, LoanApplication, LoanRepayment

admin.site.register(LoanTypes)
admin.site.register(LoanApplication)
admin.site.register(LoanRepayment)
