from django.urls import path

from .views import index, ContributionView, SharesDetailview

app_name = 'shares'

urlpatterns = [
    path('', index, name="home"),
    path('contribution/', ContributionView.as_view(), name='contribution'),
    path('details/<int:pk>/', SharesDetailview.as_view(), name='details'),
]
