from django.urls import path, include

from .views import ( RegistrationView, MembersListView, member_exit,
                    MemberDetailView, GuarantorView, MemberUpdateView)

app_name = "members"

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('list/', MembersListView.as_view(), name='list'),
    path('guarantor/', GuarantorView.as_view(), name='guarantor'),
    path('details/<int:pk>/', MemberDetailView.as_view(), name='details'),
    path('update/<int:pk>/', MemberUpdateView.as_view(), name="update"),
    path('exit/<int:pk>/', member_exit, name="exit"),
]
