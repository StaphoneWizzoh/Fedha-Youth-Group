from django.urls import path

from .views import (index, registrations, contributions, deposits, loans,
                    schedules, balances, dividends)

app_name = "administration"

urlpatterns = [
    path('', index, name='home-admin'),
    path('reg/', registrations, name='registrations'),
    path('contrib/', contributions, name='contributions'),
    path('deposits/', deposits, name='deposits'),
    path('loans/', loans, name='loans'),
    path('schedules/', schedules, name='schedules'),
    path('balances/', balances, name='balances'),
    path('dividends/', dividends, name='dividends'),
]
