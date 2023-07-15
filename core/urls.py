from django.urls import path, include

from .views import index

urlpatterns = (
    path('', index, name='home'),

    # Members app
    path('members/', include('members.urls')),

    # Loans app
    path('loans/', include('loans.urls')),

    # Shares app
    path('shares/', include('shares.urls')),

    # Blogs app
    path('blogs/', include('blogs.urls')),

    # Fedha admin app
    path('fedha/', include('administration.urls'))
)
